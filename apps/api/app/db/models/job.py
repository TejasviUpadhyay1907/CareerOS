"""Job database models — SQLite/PostgreSQL compatible."""
import uuid as _uuid
from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def _new_uuid() -> str:
    return str(_uuid.uuid4())


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    remote_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    experience_required: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    education_required: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    domain: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    seniority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    raw_description: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
    requirements = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")
    responsibilities = relationship("JobResponsibility", back_populates="job", cascade="all, delete-orphan")
    benefits = relationship("JobBenefit", back_populates="job", cascade="all, delete-orphan")
    keywords = relationship("JobKeyword", back_populates="job", cascade="all, delete-orphan")
    analysis = relationship("JobAnalysis", back_populates="job", uselist=False)
    matches = relationship("ResumeJobMatch", back_populates="job", cascade="all, delete-orphan")


class JobSkill(Base, TimestampMixin):
    __tablename__ = "job_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    importance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    job = relationship("Job", back_populates="skills")


class JobRequirement(Base, TimestampMixin):
    __tablename__ = "job_requirements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    requirement: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    job = relationship("Job", back_populates="requirements")


class JobResponsibility(Base, TimestampMixin):
    __tablename__ = "job_responsibilities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    responsibility: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    job = relationship("Job", back_populates="responsibilities")


class JobBenefit(Base, TimestampMixin):
    __tablename__ = "job_benefits"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    benefit: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    job = relationship("Job", back_populates="benefits")


class JobKeyword(Base, TimestampMixin):
    __tablename__ = "job_keywords"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    importance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    job = relationship("Job", back_populates="keywords")


class JobAnalysis(Base, TimestampMixin):
    __tablename__ = "job_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, unique=True)
    hiring_signals: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    urgency: Mapped[str] = mapped_column(String(50), nullable=False, default="normal")
    leadership_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    communication_level: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    team_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    growth_potential: Mapped[str] = mapped_column(String(50), nullable=False, default="medium")
    work_life_balance: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    company_culture_indicators: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    hidden_expectations: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    job = relationship("Job", back_populates="analysis")


class ResumeJobMatch(Base, TimestampMixin):
    __tablename__ = "resume_job_matches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False, index=True)
    resume_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    overall_match: Mapped[int] = mapped_column(Integer, nullable=False)
    technical_match: Mapped[int] = mapped_column(Integer, nullable=False)
    experience_match: Mapped[int] = mapped_column(Integer, nullable=False)
    education_match: Mapped[int] = mapped_column(Integer, nullable=False)
    project_match: Mapped[int] = mapped_column(Integer, nullable=False)
    keyword_match: Mapped[int] = mapped_column(Integer, nullable=False)
    ats_match: Mapped[int] = mapped_column(Integer, nullable=False)
    leadership_match: Mapped[int] = mapped_column(Integer, nullable=False)
    communication_match: Mapped[int] = mapped_column(Integer, nullable=False)
    industry_match: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    match_reasoning: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    job = relationship("Job", back_populates="matches")


class MatchRecommendation(Base, TimestampMixin):
    __tablename__ = "match_recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    match_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)


class ATSAnalysis(Base, TimestampMixin):
    __tablename__ = "ats_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    match_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    keyword_coverage: Mapped[int] = mapped_column(Integer, nullable=False)
    formatting_compatibility: Mapped[int] = mapped_column(Integer, nullable=False)
    action_verbs_score: Mapped[int] = mapped_column(Integer, nullable=False)
    role_alignment: Mapped[int] = mapped_column(Integer, nullable=False)
    missing_keywords: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    resume_length_score: Mapped[int] = mapped_column(Integer, nullable=False)
    section_completeness: Mapped[int] = mapped_column(Integer, nullable=False)
    optimization_potential: Mapped[int] = mapped_column(Integer, nullable=False)
    detailed_report: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class MissingSkill(Base, TimestampMixin):
    __tablename__ = "missing_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    match_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    learning_priority: Mapped[str] = mapped_column(String(50), nullable=False)
    estimated_learning_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    free_resources: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
