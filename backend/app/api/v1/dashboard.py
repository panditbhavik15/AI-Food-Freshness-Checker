"""
Dashboard endpoint — aggregated statistics for authenticated users.
"""

import json
from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.core.database import get_db
from app.api.v1.deps import get_current_user_required
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.common import success_response

router = APIRouter()


@router.get("")
def get_dashboard(
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db),
):
    """
    Get dashboard statistics for the current user.

    Returns: total scans, freshness distribution, top foods, recent activity.
    """
    user_analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id)

    # Total scans
    total_scans = user_analyses.count()

    # Freshness distribution
    freshness_rows = (
        db.query(Analysis.freshness_class, func.count(Analysis.id))
        .filter(Analysis.user_id == current_user.id)
        .group_by(Analysis.freshness_class)
        .all()
    )
    freshness_distribution = {row[0]: row[1] for row in freshness_rows}

    # Top food categories
    food_rows = (
        db.query(Analysis.food_category, func.count(Analysis.id))
        .filter(Analysis.user_id == current_user.id)
        .group_by(Analysis.food_category)
        .order_by(desc(func.count(Analysis.id)))
        .limit(5)
        .all()
    )
    top_foods = [{"name": row[0], "count": row[1]} for row in food_rows]

    # Recent analyses (last 5)
    recent = (
        user_analyses
        .order_by(desc(Analysis.created_at))
        .limit(5)
        .all()
    )
    recent_items = [
        {
            "id": a.id,
            "food_category": a.food_category,
            "freshness_class": a.freshness_class,
            "confidence": a.confidence,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in recent
    ]

    return success_response({
        "total_scans": total_scans,
        "freshness_distribution": freshness_distribution,
        "top_foods": top_foods,
        "recent_analyses": recent_items,
    })
