"""User repository."""
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    """Repository for user operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _str_id(user_id: "UUID | str") -> str:
        """Normalise a UUID to a dashed string for SQLite String(36) columns."""
        if isinstance(user_id, UUID):
            return str(user_id)
        # Make sure it has dashes even if hex was passed
        s = str(user_id)
        if len(s) == 32 and '-' not in s:
            return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:]}"
        return s

    async def get_by_id(self, user_id: "UUID | str") -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == self._str_id(user_id))
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """Update a user."""
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: "UUID | str") -> bool:
        """Delete a user."""
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False
