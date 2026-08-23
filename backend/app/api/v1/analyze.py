"""
POST /api/v1/analyze — Food freshness analysis endpoint.

Accepts an uploaded image, validates it, runs the ML pipeline,
and returns the freshness analysis result.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.deps import get_current_user_optional
from app.models.user import User
from app.schemas.common import success_response, error_response
from app.services.image_validator import validate_image, ImageValidationError
from app.services.freshness_analyzer import analyze_food_image, AnalysisError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze")
async def analyze_food(
    file: UploadFile = File(..., description="Food image (JPEG or PNG, max 10 MB)"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Analyze a food image for freshness.

    - Accepts JPEG/PNG images up to 10 MB
    - Returns food identification, freshness classification, confidence,
      visual observations, recommendation, and safety disclaimer
    - Works for both authenticated and guest users
    - Guest analyses are not persisted to history
    """
    try:
        # 1. Read file bytes
        file_bytes = await file.read()
        filename = file.filename or "upload.jpg"
        content_type = file.content_type or "application/octet-stream"

        # 2. Validate image
        try:
            image = validate_image(file_bytes, filename, content_type)
        except ImageValidationError as e:
            return error_response(e.code, e.message)

        # 3. Run analysis pipeline
        user_id = current_user.id if current_user else None
        try:
            result = analyze_food_image(image, file_bytes, db, user_id)
        except AnalysisError as e:
            return error_response(e.code, e.message)

        # 4. Return success response
        return success_response(result)

    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis.",
        )
