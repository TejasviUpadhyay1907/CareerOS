"""Main FastAPI application."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting CareerOS API")

    # Create DB tables (skip if DB is unavailable — health check still works)
    try:
        from app.db.base import Base
        from app.db.session import engine
        import app.db.models  # noqa — register all models
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables ready")
    except Exception as e:
        logger.warning(f"DB init skipped: {e}")

    yield
    logger.info("Shutting down CareerOS API")


app = FastAPI(
    title=settings.app_name,
    description="CareerOS Backend API",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "CareerOS API",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
    }


# Serve uploaded files (local dev only — in production use cloud storage)
import os
_uploads_dir = Path(os.environ.get("UPLOADS_DIR", str(Path(__file__).parent.parent / "uploads")))
try:
    _uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")
except Exception as e:
    logger.warning(f"Could not mount uploads directory: {e}")