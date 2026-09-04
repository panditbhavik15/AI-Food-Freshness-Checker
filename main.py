"""
FastAPI application entry point.

Configures middleware, CORS, routers, and startup/shutdown events.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core import settings
from app.core.database import init_db
from app.api.v1.router import router as v1_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"ML Dev Mode: {settings.ML_DEV_MODE}")

    # Initialize database tables
    init_db()
    logger.info("Database initialized")

    # Pre-warm ML inference engine
    from app.ml.inference import get_inference_engine
    engine = get_inference_engine()
    logger.info(f"ML Engine loaded: {engine.model_version} (dev_mode={engine.dev_mode})")

    # Ensure upload directory exists
    settings.upload_path.mkdir(parents=True, exist_ok=True)

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-powered visual food freshness estimation. "
        "Upload a photo of food and receive a freshness classification "
        "with confidence score, visual observations, and recommendations."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions — return safe error, log full details."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again.",
            },
        },
    )


# Mount API routes
app.include_router(v1_router)

# Serve uploaded images (for development — in production use object storage)
import os
uploads_dir = settings.UPLOAD_DIR
if os.path.isdir(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs" if settings.is_dev else None,
    }
