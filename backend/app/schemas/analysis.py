"""
Analysis Pydantic schemas — request/response models for food analysis.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    """Full analysis result returned by POST /analyze."""
    id: str
    food: str
    freshness: str
    confidence: float = Field(ge=0.0, le=1.0)
    observations: list[str]
    recommendation: str
    model_version: str
    safety_notice: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisHistoryItem(BaseModel):
    """Compact analysis record for history list."""
    id: str
    food_category: str
    freshness_class: str
    confidence: float
    thumbnail_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisDetail(BaseModel):
    """Full analysis detail for history/{id}."""
    id: str
    food_category: str
    freshness_class: str
    confidence: float
    observations: list[str]
    recommendation: str
    model_version: str
    image_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Dashboard statistics for authenticated users."""
    total_scans: int
    freshness_distribution: dict[str, int]
    top_foods: list[dict[str, int]]
    recent_analyses: list[AnalysisHistoryItem]
