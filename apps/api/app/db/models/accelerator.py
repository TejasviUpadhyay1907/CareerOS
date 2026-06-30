"""Application Accelerator database models — SQLite/PostgreSQL compatible."""
import uuid as _uuid
from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def _new_uuid() -> str:
    return str(_uuid.uuid4())


class OptimizedResume(Base, TimestampMixin):
    __tablename__ = "optimized_resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    original_resume_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    optimized_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changes: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    optimization_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estimated_ats_improvement: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estimated_match_increase: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estimated_interview_probability: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", backref="optimized_resumes")
    job = relationship("Job", backref="optimized_resumes")


class ResumeVersion(Base, TimestampMixin):
    __tablename__ = "resume_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changes_summary: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    optimization_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CoverLetter(Base, TimestampMixin):
    __tablename__ = "cover_letters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    length: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    personalization_points: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class RecruiterMessage(Base, TimestampMixin):
    __tablename__ = "recruiter_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=True, index=True)
    message_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    length: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    personalization_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_to_action: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    recipient_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    recipient_company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    platform: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class InterviewKit(Base, TimestampMixin):
    __tablename__ = "interview_kits"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    company_overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role_overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    technical_topics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    behavioral_questions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    star_suggestions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    project_questions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    resume_questions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    coding_topics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    system_design_topics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    hr_questions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    salary_tips: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    questions_to_ask: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    study_plan_90min: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    study_plan_3day: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    study_plan_7day: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    priority_ranking: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class InterviewQuestion(Base, TimestampMixin):
    __tablename__ = "interview_questions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    kit_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_kits.id"), nullable=False, index=True)
    question_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    question: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suggested_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class StudyPlan(Base, TimestampMixin):
    __tablename__ = "study_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    kit_id: Mapped[str] = mapped_column(String(36), ForeignKey("interview_kits.id"), nullable=False, index=True)
    plan_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tasks: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    resources: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    milestones: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class GeneratedDocument(Base, TimestampMixin):
    __tablename__ = "generated_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    document_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    document_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    format: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    export_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class DocumentVersion(Base, TimestampMixin):
    __tablename__ = "document_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    document_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    document_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changes: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    generation_extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class GenerationHistory(Base, TimestampMixin):
    __tablename__ = "generation_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    generation_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    input_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    output_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    success: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
