"""Database session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

_db_url = settings.database_url

try:
    if _db_url.startswith("sqlite"):
        engine = create_async_engine(_db_url, echo=settings.debug)
    else:
        connect_args = {"ssl": "require"} if "supabase.co" in _db_url else {}
        engine = create_async_engine(
            _db_url,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            echo=settings.debug,
            connect_args=connect_args,
        )
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
except Exception as e:
    import logging
    logging.warning(f"DB engine creation failed: {e} — using in-memory SQLite fallback")
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
