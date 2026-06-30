"""Storage service — local filesystem for dev, Supabase for production."""
import os
import uuid
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Local uploads directory
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"


class StorageService:
    """File storage — uses local filesystem when Supabase is not configured."""

    def __init__(self):
        self._use_supabase = bool(
            settings.supabase_url
            and settings.supabase_url != "your_supabase_url"
            and settings.supabase_service_role_key
            and settings.supabase_service_role_key != "your_supabase_service_role_key"
        )
        self._client = None

    async def initialize(self) -> None:
        if self._use_supabase:
            try:
                from supabase import create_client
                self._client = create_client(
                    settings.supabase_url,
                    settings.supabase_service_role_key,
                )
                logger.info("Storage: using Supabase")
            except Exception as e:
                logger.warning(f"Supabase init failed, falling back to local: {e}")
                self._use_supabase = False
        if not self._use_supabase:
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage: using local filesystem at {UPLOAD_DIR}")

    async def upload_file(
        self,
        file_content: bytes,
        original_filename: str,
        user_id: str,
        mime_type: str,
    ) -> tuple[str, str]:
        """Upload file. Returns (storage_path, public_url)."""
        ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else "bin"
        unique_name = f"{uuid.uuid4()}.{ext}"
        relative_path = f"{user_id}/{unique_name}"

        if self._use_supabase and self._client:
            return await self._upload_supabase(file_content, relative_path, mime_type)
        else:
            return await self._upload_local(file_content, relative_path)

    async def _upload_local(self, content: bytes, relative_path: str) -> tuple[str, str]:
        dest = UPLOAD_DIR / relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        # Return a path that the API can serve
        storage_url = f"http://localhost:{settings.port}/uploads/{relative_path}"
        logger.info(f"Saved file locally: {dest}")
        return str(relative_path), storage_url

    async def _upload_supabase(self, content: bytes, path: str, mime_type: str) -> tuple[str, str]:
        bucket = "resumes"
        self._client.storage.from_(bucket).upload(
            path=path,
            file=content,
            file_options={"content-type": mime_type},
        )
        url = f"{settings.supabase_url}/storage/v1/object/public/{bucket}/{path}"
        return f"{bucket}/{path}", url

    async def delete_file(self, storage_path: str) -> None:
        if self._use_supabase and self._client:
            bucket, path = storage_path.split("/", 1) if "/" in storage_path else ("resumes", storage_path)
            self._client.storage.from_(bucket).remove([path])
        else:
            local = UPLOAD_DIR / storage_path
            if local.exists():
                local.unlink()

    async def get_file_url(self, storage_path: str) -> str:
        if self._use_supabase:
            return f"{settings.supabase_url}/storage/v1/object/public/{storage_path}"
        return f"http://localhost:{settings.port}/uploads/{storage_path}"


storage_service = StorageService()
