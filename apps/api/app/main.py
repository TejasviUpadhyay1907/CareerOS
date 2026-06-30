"""Main FastAPI application."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.db.session import AsyncSessionLocal
from app.services.demo_seeder import seed_demo_data

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting CareerOS API")

    # Auto-create all tables from current SQLAlchemy models (dev mode)
    # This ensures the DB schema always matches the ORM models
    from app.db.base import Base
    from app.db.session import engine
    import app.db.models  # noqa — register all models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables verified/created")

    # Seed demo data if demo mode is enabled
    if settings.demo_mode:
        logger.info("Demo mode enabled, seeding demo data...")
        async with AsyncSessionLocal() as db:
            try:
                await seed_demo_data(db)
            except Exception as e:
                logger.error(f"Failed to seed demo data: {e}", exc_info=True)

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


# Serve uploaded files (local dev only)
_uploads_dir = Path(__file__).parent.parent / "uploads"
_uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")