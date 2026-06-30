"""Base database model — SQLite/PostgreSQL compatible."""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base model for all database models."""
    pass


class TimestampMixin:
    """Mixin for created_at / updated_at fields."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now(), onupdate=func.now(), nullable=False
    )


# Kept for backwards-compatibility — new models define their own id column
class UUIDMixin:
    """Mixin for a String(36) UUID primary key."""

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
