"""Pydantic models for job-related operations."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# Request Models
class JobAnalyzeRequest(BaseModel):
    """Request model for job analysis."""

    job_description: str = Field(..., min_length=10, description="Raw job description text")
    resume_id: str = Field(..., description="Resume ID to match against")


class JobMatchRequest(BaseModel):
    """Request model for job matching."""

    job_id: str = Field(..., description="Job ID")
    resume_id: str = Field(..., description="Resume ID")


# Response Models
class JobSkillResponse(BaseModel):
    """Response model for job skill."""

    name: str
    category: str
    type: str
    importance: Optional[int] = None


class JobRequirementResponse(BaseModel):
    """Response model for job requirement."""

    requirement: str
    category: Optional[str] = None
    is_mandatory: bool


class JobResponsibilityResponse(BaseModel):
    """Response model for job responsibility."""

    responsibility: str
    priority: Optional[int] = None


class JobBenefitResponse(BaseModel):
    """Response model for job benefit."""

    benefit: str
    category: Optional[str] = None


class JobAnalysisResponse(BaseModel):
    """Response model for job analysis."""

    hiring_signals: list[str]
    urgency: str
    leadership_required: bool
    communication_level: str
    team_size: Optional[str] = None
    growth_potential: str
    work_life_balance: str
    company_culture_indicators: list[str]
    hidden_expectations: list[str]


class JobResponse(BaseModel):
    """Response model for job."""

    id: str
    user_id: str
    title: str
    company_name: str
    department: Optional[str] = None
    employment_type: Optional[str] = None
    location: Optional[str] = None
    remote_status: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    industry: Optional[str] = None
    domain: Optional[str] = None
    seniority: Optional[str] = None
    raw_description: str
    parsed_data: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class JobDetailResponse(BaseModel):
    """Response model for job details."""

    job: JobResponse
    skills: list[JobSkillResponse]
    requirements: list[JobRequirementResponse]
    responsibilities: list[JobResponsibilityResponse]
    benefits: list[JobBenefitResponse]
    analysis: Optional[JobAnalysisResponse] = None


class MatchReasoning(BaseModel):
    """Response model for match reasoning."""

    technical: str
    experience: str
    education: str
    project: str
    keyword: str
    ats: str
    leadership: str
    communication: str
    industry: str


class ResumeJobMatchResponse(BaseModel):
    """Response model for resume-job match."""

    id: str
    job_id: str
    resume_id: str
    overall_match: int
    technical_match: int
    experience_match: int
    education_match: int
    project_match: int
    keyword_match: int
    ats_match: int
    leadership_match: int
    communication_match: int
    industry_match: int
    confidence_score: int
    match_reasoning: MatchReasoning
    created_at: datetime


class MissingSkillResponse(BaseModel):
    """Response model for missing skill."""

    skill_name: str
    category: str
    learning_priority: str
    estimated_learning_time: Optional[str] = None
    difficulty: Optional[str] = None
    free_resources: list[str]


class ATSAnalysisResponse(BaseModel):
    """Response model for ATS analysis."""

    keyword_coverage: int
    formatting_compatibility: int
    action_verbs_score: int
    role_alignment: int
    missing_keywords: list[str]
    resume_length_score: int
    section_completeness: int
    optimization_potential: int
    detailed_report: dict[str, Any]


class MatchRecommendationResponse(BaseModel):
    """Response model for match recommendation."""

    recommendation: str
    category: str
    priority: str
    action_type: str


class InsightsResponse(BaseModel):
    """Response model for AI insights."""

    top_strengths: list[str]
    biggest_weaknesses: list[str]
    reasons_recruiter_may_reject: list[str]
    reasons_recruiter_may_shortlist: list[str]
    hidden_expectations: list[str]
    resume_gaps: list[str]
    experience_gaps: list[str]
    suggested_resume_changes: list[str]
    suggested_projects: list[str]
    suggested_certifications: list[str]
    suggested_technologies: list[str]
    suggested_interview_topics: list[str]


class JobAnalyzeResponse(BaseModel):
    """Response model for job analysis."""

    job: JobDetailResponse
    match: ResumeJobMatchResponse
    missing_skills: list[MissingSkillResponse]
    ats_analysis: ATSAnalysisResponse
    insights: InsightsResponse
