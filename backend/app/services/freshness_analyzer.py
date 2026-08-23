"""
Freshness analyzer service — orchestrates the full analysis pipeline.

Coordinates image validation → ML inference → recommendation generation.
"""

import json
import logging
import uuid
from pathlib import Path

from PIL import Image
from sqlalchemy.orm import Session

from app.core import settings
from app.ml.inference import get_inference_engine
from app.models.analysis import Analysis
from app.services.recommendation import get_recommendation, SAFETY_NOTICE
from app.utils.image_utils import strip_exif, create_thumbnail, save_image

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Raised when analysis fails."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


def analyze_food_image(
    image: Image.Image,
    file_bytes: bytes,
    db: Session,
    user_id: str | None = None,
) -> dict:
    """
    Run the full food freshness analysis pipeline.

    Steps:
    1. Strip EXIF data from image
    2. Run ML inference (food identification + freshness classification)
    3. Handle out-of-distribution cases
    4. Generate recommendation and observations
    5. Persist result (if authenticated user)
    6. Return structured result

    Args:
        image: Validated PIL Image
        file_bytes: Original file bytes for storage
        db: Database session
        user_id: Authenticated user ID (None for guest)

    Returns:
        Dict with full analysis result
    """
    # 1. Strip EXIF data
    clean_image = strip_exif(image)

    # 2. Run ML inference
    engine = get_inference_engine()
    prediction = engine.predict(clean_image)

    # 3. Handle non-food or unsupported food
    if not prediction.is_food or not prediction.is_supported:
        raise AnalysisError(
            "UNSUPPORTED_CONTENT",
            "Unable to identify a supported food item. "
            "Please upload a clear image of one of these foods: "
            "apple, banana, tomato, potato, orange, carrot, cucumber, or strawberry.",
        )

    # 4. Generate recommendation and observations
    result = get_recommendation(prediction.food_category, prediction.freshness_class)

    # 5. Save image and create thumbnail
    image_id = str(uuid.uuid4())
    image_path = save_image(file_bytes, image_id)
    thumbnail_path = create_thumbnail(clean_image, image_id)

    # 6. Determine confidence tier and add warning if low
    confidence_warning = ""
    if prediction.confidence < 0.50:
        confidence_warning = " This result has low confidence. Consider uploading a clearer image."

    # 7. Persist to database (only for authenticated users)
    analysis_record = Analysis(
        id=image_id,
        user_id=user_id,
        image_path=str(image_path),
        thumbnail_path=str(thumbnail_path) if thumbnail_path else None,
        food_category=prediction.food_category.capitalize(),
        freshness_class=prediction.freshness_class,
        confidence=prediction.confidence,
        observations=json.dumps(result.observations),
        recommendation=result.recommendation + confidence_warning,
        model_version=prediction.model_version,
    )

    if user_id:
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
    else:
        # For guest users, still add to session for the response but don't necessarily persist long-term
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

    # 8. Build response
    return {
        "id": analysis_record.id,
        "food": prediction.food_category.capitalize(),
        "freshness": prediction.freshness_class,
        "confidence": prediction.confidence,
        "observations": result.observations,
        "recommendation": result.recommendation + confidence_warning,
        "model_version": prediction.model_version,
        "safety_notice": result.safety_notice,
        "created_at": analysis_record.created_at.isoformat(),
    }
