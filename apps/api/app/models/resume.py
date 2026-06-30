"""Pydantic models for resume API."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class ResumeUploadRequest(BaseModel):
    """Request model for resume upload."""

    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., gt=0, le=10 * 1024 * 1024, description="File size in bytes (max 10MB)")
    mime_type: str = Field(..., description="MIME type of the file")

    @field_validator("mime_type")
    @classmethod
    def validate_mime_type(cls, v: str) -> str:
        """Validate MIME type is PDF or DOCX."""
        allowed_types = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        if v.lower() not in allowed_types:
            raise ValueError(f"Invalid file type. Allowed types: {', '.join(allowed_types)}")
        return v.lower()


class ResumeUploadResponse(BaseModel):
    """Response model for resume upload."""

    id: str
    original_filename: str
    storage_url: str
    file_size: int
    mime_type: str
    created_at: datetime


class ResumeResponse(BaseModel):
    """Response model for resume."""

    id: str
    user_id: str
    original_filename: str
    storage_url: str
    file_size: int
    mime_type: str
    is_primary: bool
    raw_text: Optional[str] = None
    parsed_data: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class Skill(BaseModel):
    """Skill model."""

    name: str
    category: str
    proficiency: Optional[str] = None
    years_experience: Optional[int] = None
    is_primary: bool = False


class Experience(BaseModel):
    """Experience model."""

    company: str
    title: str
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    achievements: Optional[list[str]] = None


class Education(BaseModel):
    """Education model."""

    institution: str
    degree: str
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None
    honors: Optional[list[str]] = None


class Project(BaseModel):
    """Project model."""

    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    technologies: list[str]
    achievements: Optional[list[str]] = None


class Certification(BaseModel):
    """Certification model."""

    name: str
    issuer: str
    issue_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    url: Optional[str] = None


class Language(BaseModel):
    """Language model."""

    name: str
    proficiency: str


class Achievement(BaseModel):
    """Achievement model."""

    title: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    category: Optional[str] = None


class Link(BaseModel):
    """Link model."""

    type: str
    url: str
    label: Optional[str] = None


class ResumeMetadataResponse(BaseModel):
    """Response model for resume metadata."""

    years_of_experience: Optional[int] = None
    primary_domain: Optional[str] = None
    career_level: Optional[str] = None
    total_projects: int = 0
    total_certifications: int = 0
    total_achievements: int = 0
    has_leadership_experience: bool = False
    has_open_source_contributions: bool = False
    has_internships: bool = False
    has_research_experience: bool = False
    has_publications: bool = False


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis."""

    health_score: int
    health_breakdown: dict[str, int]
    recommendations: list[str]
    strengths: list[str]
    weaknesses: list[str]
    missing_sections: list[str]
    ats_score: Optional[int] = None
    formatting_score: Optional[int] = None
    readability_score: Optional[int] = None


class ResumeDetailResponse(BaseModel):
    """Detailed response model for resume with all related data."""

    resume: ResumeResponse
    metadata: Optional[ResumeMetadataResponse] = None
    analysis: Optional[ResumeAnalysisResponse] = None
    skills: list[Skill] = []
    experience: list[Experience] = []
    education: list[Education] = []
    projects: list[Project] = []
    certifications: list[Certification] = []
    languages: list[Language] = []
    achievements: list[Achievement] = []
    links: list[Link] = []


class ResumeAnalyzeRequest(BaseModel):
    """Request model for resume analysis."""

    resume_id: str


class ResumeAnalyzeResponse(BaseModel):
    """Response model for resume analysis."""

    resume_id: str
    analysis: ResumeAnalysisResponse
    metadata: ResumeMetadataResponse


class ResumeSummaryRequest(BaseModel):
    """Request model for resume summary."""

    resume_id: str


class ResumeSummaryResponse(BaseModel):
    """Response model for resume summary."""

    professional_summary: str
    career_highlights: list[str]
    top_strengths: list[str]
    potential_weaknesses: list[str]
    career_level: str
    primary_technology_stack: list[str]
    suggested_job_roles: list[str]
    suggested_industries: list[str]
    top_keywords: list[str]
