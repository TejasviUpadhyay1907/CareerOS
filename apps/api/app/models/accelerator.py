"""Pydantic models for application accelerator operations."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# Request Models
class ResumeOptimizeRequest(BaseModel):
    """Request to optimize resume."""

    resume_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)


class CoverLetterGenerateRequest(BaseModel):
    """Request to generate cover letter."""

    resume_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    tone: str = Field(default="professional")
    length: str = Field(default="medium")


class RecruiterOutreachRequest(BaseModel):
    """Request to generate recruiter outreach."""

    resume_id: str = Field(..., min_length=1)
    job_id: Optional[str] = None
    message_type: str = Field(default="linkedin_connection")
    tone: str = Field(default="professional")
    length: str = Field(default="medium")


class InterviewGenerateRequest(BaseModel):
    """Request to generate interview kit."""

    resume_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)


class DocumentExportRequest(BaseModel):
    """Request to export document."""

    document_id: str = Field(..., min_length=1)
    format: str = Field(default="markdown")


# Response Models
class ResumeChange(BaseModel):
    """Resume change detail."""

    original: str
    optimized: str
    reason: str
    ats_improvement: str
    recruiter_impact: str


class SkillsOptimization(BaseModel):
    """Skills optimization detail."""

    original_order: list[str]
    optimized_order: list[str]
    reasoning: str


class KeywordAddition(BaseModel):
    """Keyword addition detail."""

    keyword: str
    where_added: str
    reason: str


class ResumeOptimizeResponse(BaseModel):
    """Resume optimization response."""

    id: str
    optimized_summary: str
    optimized_experience: list[ResumeChange]
    optimized_skills: SkillsOptimization
    optimized_projects: list[ResumeChange]
    keyword_additions: list[KeywordAddition]
    optimization_score: int
    estimated_ats_improvement: int
    estimated_match_increase: int
    estimated_interview_probability: int
    created_at: datetime


class PersonalizationPoint(BaseModel):
    """Personalization point."""

    point: str
    source: str


class CoverLetterResponse(BaseModel):
    """Cover letter response."""

    id: str
    content: str
    tone: str
    length: str
    company_name: str
    role_title: str
    personalization_points: list[PersonalizationPoint]
    created_at: datetime


class RecruiterMessageResponse(BaseModel):
    """Recruiter message response."""

    id: str
    message_type: str
    subject: Optional[str]
    content: str
    tone: str
    length: str
    personalization_reason: str
    call_to_action: str
    recipient_name: Optional[str]
    recipient_company: Optional[str]
    platform: str
    created_at: datetime


class TechnicalTopic(BaseModel):
    """Technical topic."""

    topic: str
    priority: str
    resources: list[str]


class BehavioralQuestion(BaseModel):
    """Behavioral question."""

    question: str
    star_suggestion: str
    priority: str


class ProjectQuestion(BaseModel):
    """Project question."""

    question: str
    suggested_answer: str
    priority: str


class CodingTopic(BaseModel):
    """Coding topic."""

    topic: str
    priority: str
    practice_problems: list[str]


class SystemDesignTopic(BaseModel):
    """System design topic."""

    topic: str
    priority: str
    key_concepts: list[str]


class QuestionToAsk(BaseModel):
    """Question to ask interviewer."""

    question: str
    reason: str


class StudyPlanItem(BaseModel):
    """Study plan item."""

    time: Optional[str] = None
    task: str
    priority: str


class StudyPlanDay(BaseModel):
    """Study plan day."""

    day: str
    tasks: list[str]
    focus: str


class PriorityRanking(BaseModel):
    """Priority ranking."""

    highest_priority: list[str]
    high_priority: list[str]
    medium_priority: list[str]
    low_priority: list[str]


class InterviewKitResponse(BaseModel):
    """Interview kit response."""

    id: str
    company_name: str
    role_title: str
    company_overview: str
    role_overview: str
    responsibilities: list[str]
    technical_topics: list[TechnicalTopic]
    behavioral_questions: list[BehavioralQuestion]
    project_questions: list[ProjectQuestion]
    resume_questions: list[ProjectQuestion]
    coding_topics: list[CodingTopic]
    system_design_topics: list[SystemDesignTopic]
    hr_questions: list[dict[str, str]]
    salary_tips: list[str]
    questions_to_ask: list[QuestionToAsk]
    study_plan_90min: list[StudyPlanItem]
    study_plan_3day: list[StudyPlanDay]
    study_plan_7day: list[StudyPlanDay]
    priority_ranking: PriorityRanking
    created_at: datetime


class GeneratedDocumentResponse(BaseModel):
    """Generated document response."""

    id: str
    document_type: str
    title: str
    description: Optional[str]
    format: str
    file_path: Optional[str]
    file_size: Optional[int]
    export_count: int
    created_at: datetime


class DocumentExportResponse(BaseModel):
    """Document export response."""

    file_path: str
    format: str
    file_size: int
