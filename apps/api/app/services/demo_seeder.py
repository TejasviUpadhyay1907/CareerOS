"""Demo data seeder for demo mode.

Seeds minimal demo data so judges can explore the system without uploading files.
All data is skipped if models/tables don't exist (graceful degradation).
"""
import uuid
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"
DEMO_RESUME_ID = "00000000-0000-0000-0000-000000000002"
DEMO_JOB_ID = "00000000-0000-0000-0000-000000000003"
DEMO_APPLICATION_ID = "00000000-0000-0000-0000-000000000004"
DEMO_COMPANY_ID = "00000000-0000-0000-0000-000000000005"


async def _table_exists(db: AsyncSession, table_name: str) -> bool:
    """Check if a table exists in the database."""
    try:
        result = await db.execute(
            text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        )
        return result.scalar() is not None
    except Exception:
        return False


async def seed_demo_data(db: AsyncSession) -> None:
    """Seed demo data if demo mode is enabled."""
    if not settings.demo_mode:
        return

    logger.info("Seeding demo data...")

    try:
        # Seed user
        if await _table_exists(db, "users"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO users
                        (id, email, password_hash, first_name, last_name, email_verified, subscription_tier, created_at, updated_at)
                    VALUES
                        (:id, :email, :pw, :fn, :ln, 1, 'pro', :now, :now)
                """),
                {
                    "id": DEMO_USER_ID,
                    "email": "demo@careeros.ai",
                    "pw": "$2b$12$xUgTkDTOwetItlhGZRQiuutkVrxS1Tu.AzC/y39ITpgMhG80QbNWa",  # Demo1234!
                    "fn": "Demo",
                    "ln": "User",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed resume
        if await _table_exists(db, "resumes"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO resumes
                        (id, user_id, original_filename, storage_path, storage_url, file_size, mime_type,
                         is_primary, is_deleted, raw_text, created_at, updated_at)
                    VALUES
                        (:id, :uid, :fn, :sp, :su, :fs, :mt, 1, 0, :rt, :now, :now)
                """),
                {
                    "id": DEMO_RESUME_ID,
                    "uid": DEMO_USER_ID,
                    "fn": "demo_resume.pdf",
                    "sp": "resumes/demo/resume.pdf",
                    "su": "https://example.com/demo_resume.pdf",
                    "fs": 102400,
                    "mt": "application/pdf",
                    "rt": "John Demo\nSenior Software Engineer\nSan Francisco, CA\n5+ years experience in full-stack development.",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed company profile
        if await _table_exists(db, "company_profiles"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO company_profiles
                        (id, user_id, name, website, industry, size, location, description, is_deleted, created_at, updated_at)
                    VALUES
                        (:id, :uid, :name, :web, :ind, :sz, :loc, :desc, 0, :now, :now)
                """),
                {
                    "id": DEMO_COMPANY_ID,
                    "uid": DEMO_USER_ID,
                    "name": "Acme Corp",
                    "web": "https://acmecorp.example.com",
                    "ind": "Technology",
                    "sz": "1001-5000",
                    "loc": "San Francisco, CA",
                    "desc": "A leading technology company building innovative products.",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed job
        if await _table_exists(db, "jobs"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO jobs
                        (id, user_id, title, company_name, employment_type, location, remote_status,
                         experience_required, raw_description, is_deleted, created_at, updated_at)
                    VALUES
                        (:id, :uid, :title, :co, :et, :loc, :rs, :exp, :rd, 0, :now, :now)
                """),
                {
                    "id": DEMO_JOB_ID,
                    "uid": DEMO_USER_ID,
                    "title": "Senior Software Engineer",
                    "co": "Acme Corp",
                    "et": "full_time",
                    "loc": "San Francisco, CA",
                    "rs": "hybrid",
                    "exp": "5+ years",
                    "rd": "We are looking for a Senior Software Engineer to join our growing team...",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed application
        if await _table_exists(db, "applications"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO applications
                        (id, user_id, resume_id, job_id, company_id, status, priority, probability,
                         notes, is_deleted, created_at, updated_at)
                    VALUES
                        (:id, :uid, :rid, :jid, :cid, :st, :pr, :prob, :notes, 0, :now, :now)
                """),
                {
                    "id": DEMO_APPLICATION_ID,
                    "uid": DEMO_USER_ID,
                    "rid": DEMO_RESUME_ID,
                    "jid": DEMO_JOB_ID,
                    "cid": DEMO_COMPANY_ID,
                    "st": "interview",
                    "pr": "high",
                    "prob": 75,
                    "notes": "Strong technical interview. Waiting for HR round.",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed notification
        if await _table_exists(db, "notifications"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO notifications
                        (id, user_id, application_id, notification_type, title, message,
                         priority, is_read, is_deleted, created_at, updated_at)
                    VALUES
                        (:id, :uid, :aid, :nt, :title, :msg, :pr, 0, 0, :now, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "uid": DEMO_USER_ID,
                    "aid": DEMO_APPLICATION_ID,
                    "nt": "interview_reminder",
                    "title": "Interview Tomorrow",
                    "msg": "Your interview with Acme Corp is scheduled for tomorrow at 2 PM. Good luck!",
                    "pr": "high",
                    "now": datetime.utcnow().isoformat(),
                },
            )

        # Seed timeline event
        if await _table_exists(db, "timeline_events"):
            await db.execute(
                text("""
                    INSERT OR IGNORE INTO timeline_events
                        (id, application_id, event_type, title, description,
                         event_date, is_deleted, created_at, updated_at)
                    VALUES
                        (:id, :aid, :et, :title, :desc, :ed, 0, :now, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "aid": DEMO_APPLICATION_ID,
                    "et": "application_submitted",
                    "title": "Application Submitted",
                    "desc": "Applied for Senior Software Engineer at Acme Corp",
                    "ed": (datetime.utcnow() - timedelta(days=14)).isoformat(),
                    "now": datetime.utcnow().isoformat(),
                },
            )

        await db.commit()
        logger.info("Demo data seeded successfully")

    except Exception as e:
        logger.error(f"Failed to seed demo data: {e}", exc_info=True)
        await db.rollback()
        # Don't crash the app on seeding failure
