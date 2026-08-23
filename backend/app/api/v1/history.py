"""
History endpoints — view and manage past analyses.

All endpoints require authentication.
Users can only access their own history (data isolation enforced at query level).
"""

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.api.v1.deps import get_current_user_required
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.common import success_response, error_response
from app.services.recommendation import SAFETY_NOTICE

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
def get_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of the user's past analyses.

    Returns compact history items with food, freshness, confidence, and date.
    """
    offset = (page - 1) * page_size

    # Query only this user's analyses (data isolation)
    total = db.query(Analysis).filter(Analysis.user_id == current_user.id).count()

    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(desc(Analysis.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    items = [
        {
            "id": a.id,
            "food_category": a.food_category,
            "freshness_class": a.freshness_class,
            "confidence": a.confidence,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in analyses
    ]

    return success_response({
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
    })


@router.get("/{analysis_id}")
def get_analysis_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    """
    Get full details of a specific analysis.

    Returns all fields including observations, recommendation, and model version.
    """
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )

    if not analysis:
        return error_response("NOT_FOUND", "Analysis not found.")

    try:
        observations = json.loads(analysis.observations)
    except (json.JSONDecodeError, TypeError):
        observations = []

    return success_response({
        "id": analysis.id,
        "food_category": analysis.food_category,
        "freshness_class": analysis.freshness_class,
        "confidence": analysis.confidence,
        "observations": observations,
        "recommendation": analysis.recommendation,
        "model_version": analysis.model_version,
        "safety_notice": SAFETY_NOTICE,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    })


@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    """
    Delete a specific analysis record.

    Users can only delete their own analyses.
    """
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )

    if not analysis:
        return error_response("NOT_FOUND", "Analysis not found.")

    db.delete(analysis)
    db.commit()

    logger.info(f"Analysis {analysis_id} deleted by user {current_user.id}")

    return success_response({"message": "Analysis deleted successfully."})
