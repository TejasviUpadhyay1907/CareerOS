"""Resume database models — SQLite/PostgreSQL compatible."""
import uuid as _uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def _new_uuid() -> str:
    return str(_uuid.uuid4())


class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    analysis = relationship("ResumeAnalysis", back_populates="resume", uselist=False)
    meta_data = relationship("ResumeMetadata", back_populates="resume", uselist=False)
    skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    experience = relationship("ResumeExperience", back_populates="resume", cascade="all, delete-orphan")
    education = relationship("ResumeEducation", back_populates="resume", cascade="all, delete-orphan")
    projects = relationship("ResumeProject", back_populates="resume", cascade="all, delete-orphan")
    certifications = relationship("ResumeCertification", back_populates="resume", cascade="all, delete-orphan")
    languages = relationship("ResumeLanguage", back_populates="resume", cascade="all, delete-orphan")
    achievements = relationship("ResumeAchievement", back_populates="resume", cascade="all, delete-orphan")
    links = relationship("ResumeLink", back_populates="resume", cascade="all, delete-orphan")


class ResumeAnalysis(Base, TimestampMixin):
    __tablename__ = "resume_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, unique=True)
    health_score: Mapped[int] = mapped_column(Integer, nullable=False)
    health_breakdown: Mapped[dict] = mapped_column(JSON, nullable=False)
    recommendations: Mapped[list] = mapped_column(JSON, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, nullable=False)
    weaknesses: Mapped[list] = mapped_column(JSON, nullable=False)
    missing_sections: Mapped[list] = mapped_column(JSON, nullable=False)
    ats_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    formatting_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    readability_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    resume = relationship("Resume", back_populates="analysis")


class ResumeMetadata(Base, TimestampMixin):
    __tablename__ = "resume_metadata"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, unique=True)
    years_of_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    primary_domain: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    career_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    total_projects: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_certifications: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_achievements: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_leadership_experience: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_open_source_contributions: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_internships: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_research_experience: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_publications: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", back_populates="meta_data")


class ResumeSkill(Base, TimestampMixin):
    __tablename__ = "resume_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    proficiency: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    years_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    resume = relationship("Resume", back_populates="skills")


class ResumeExperience(Base, TimestampMixin):
    __tablename__ = "resume_experience"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    achievements: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    resume = relationship("Resume", back_populates="experience")


class ResumeEducation(Base, TimestampMixin):
    __tablename__ = "resume_education"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    institution: Mapped[str] = mapped_column(String(200), nullable=False)
    degree: Mapped[str] = mapped_column(String(200), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    gpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    honors: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    resume = relationship("Resume", back_populates="education")


class ResumeProject(Base, TimestampMixin):
    __tablename__ = "resume_projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    technologies: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    achievements: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    resume = relationship("Resume", back_populates="projects")


class ResumeCertification(Base, TimestampMixin):
    __tablename__ = "resume_certifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    issuer: Mapped[str] = mapped_column(String(200), nullable=False)
    issue_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expiration_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    credential_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    resume = relationship("Resume", back_populates="certifications")


class ResumeLanguage(Base, TimestampMixin):
    __tablename__ = "resume_languages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency: Mapped[str] = mapped_column(String(50), nullable=False)

    resume = relationship("Resume", back_populates="languages")


class ResumeAchievement(Base, TimestampMixin):
    __tablename__ = "resume_achievements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    resume = relationship("Resume", back_populates="achievements")


class ResumeLink(Base, TimestampMixin):
    __tablename__ = "resume_links"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    resume = relationship("Resume", back_populates="links")
