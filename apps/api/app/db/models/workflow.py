"""Workflow Engine database models."""
import uuid as _uuid

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin

# Use String(36) UUIDs for SQLite compatibility
_UUID = String(36)


def _new_uuid():
    return str(_uuid.uuid4())


class Application(Base, TimestampMixin):
    """Application / Career Case."""

    __tablename__ = "applications"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    resume_id = Column(_UUID, ForeignKey("resumes.id"), nullable=False, index=True)
    job_id = Column(_UUID, ForeignKey("jobs.id"), nullable=True, index=True)
    company_id = Column(_UUID, ForeignKey("company_profiles.id"), nullable=True, index=True)
    status = Column(String(50), default="wishlist")
    stage = Column(String(100))
    priority = Column(String(50), default="medium")
    probability = Column(Integer, default=50)
    notes = Column(Text)
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", backref="applications")
    job = relationship("Job", backref="applications")
    company = relationship("CompanyProfile", backref="applications")


class ApplicationEvent(Base, TimestampMixin):
    """Application lifecycle events."""

    __tablename__ = "application_events"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    event_type = Column(String(100))
    event_data = Column(JSON)
    description = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)


class ApplicationTask(Base, TimestampMixin):
    """Tasks associated with applications."""

    __tablename__ = "application_tasks"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255))
    description = Column(Text)
    due_date = Column(DateTime)
    priority = Column(String(50))
    status = Column(String(50), default="pending")
    task_type = Column(String(100))
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class ApplicationNote(Base, TimestampMixin):
    """Notes for applications."""

    __tablename__ = "application_notes"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text)
    note_type = Column(String(50))
    is_deleted = Column(Boolean, default=False, nullable=False)


class ApplicationDocument(Base, TimestampMixin):
    """Documents linked to applications."""

    __tablename__ = "application_documents"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    document_type = Column(String(100))
    document_id = Column(_UUID)
    version = Column(Integer, default=1)
    file_path = Column(String(500))
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class ApplicationStatusHistory(Base, TimestampMixin):
    """Status change history."""

    __tablename__ = "application_status_history"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    old_status = Column(String(50))
    new_status = Column(String(50))
    reason = Column(Text)
    changed_by = Column(String(100))
    is_deleted = Column(Boolean, default=False, nullable=False)


class ApplicationFollowup(Base, TimestampMixin):
    """Follow-up reminders."""

    __tablename__ = "application_followups"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    scheduled_date = Column(DateTime)
    followup_type = Column(String(100))
    status = Column(String(50), default="pending")
    message = Column(Text)
    ai_suggested = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False, nullable=False)


class CompanyProfile(Base, TimestampMixin):
    """Company profiles."""

    __tablename__ = "company_profiles"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255))
    website = Column(String(500))
    industry = Column(String(100))
    size = Column(String(50))
    location = Column(String(255))
    description = Column(Text)
    notes = Column(Text)
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class Contact(Base, TimestampMixin):
    """Contacts at companies."""

    __tablename__ = "contacts"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(_UUID, ForeignKey("company_profiles.id"), nullable=True, index=True)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=True, index=True)
    name = Column(String(255))
    role = Column(String(255))
    email = Column(String(255))
    phone = Column(String(100))
    linkedin = Column(String(500))
    notes = Column(Text)
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class ActivityLog(Base, TimestampMixin):
    """User activity logs."""

    __tablename__ = "activity_logs"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=True, index=True)
    action = Column(String(100))
    entity_type = Column(String(100))
    entity_id = Column(_UUID)
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class TimelineEvent(Base, TimestampMixin):
    """Timeline events for applications."""

    __tablename__ = "timeline_events"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=False, index=True)
    event_type = Column(String(100))
    title = Column(String(255))
    description = Column(Text)
    event_date = Column(DateTime)
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)


class Notification(Base, TimestampMixin):
    """User notifications."""

    __tablename__ = "notifications"

    id = Column(_UUID, primary_key=True, default=_new_uuid)
    user_id = Column(_UUID, ForeignKey("users.id"), nullable=False, index=True)
    application_id = Column(_UUID, ForeignKey("applications.id"), nullable=True, index=True)
    notification_type = Column(String(100))
    title = Column(String(255))
    message = Column(Text)
    priority = Column(String(50))
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500))
    extra_metadata = Column(JSON)
    is_deleted = Column(Boolean, default=False, nullable=False)
