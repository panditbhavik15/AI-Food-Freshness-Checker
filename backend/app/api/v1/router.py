"""
API v1 aggregated router — mounts all v1 endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.analyze import router as analyze_router
from app.api.v1.auth import router as auth_router
from app.api.v1.history import router as history_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.health import router as health_router

router = APIRouter(prefix="/api/v1")

router.include_router(analyze_router, tags=["Analysis"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(history_router, prefix="/history", tags=["History"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(health_router, tags=["Health"])
