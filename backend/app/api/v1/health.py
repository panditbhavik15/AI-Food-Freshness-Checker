"""
Health check endpoint.
"""

from fastapi import APIRouter

from app.core import settings
from app.ml.inference import get_inference_engine

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.

    Returns application status, environment, and ML model status.
    """
    engine = get_inference_engine()

    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "ml_model": {
            "version": engine.model_version,
            "dev_mode": engine.dev_mode,
        },
    }
