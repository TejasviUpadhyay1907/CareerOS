"""Pydantic models for workflow engine operations."""
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Application Models
class ApplicationCreate(BaseModel):
    """Request model for creating application."""

    resume_id: UUID
    job_id: Optional[UUID] = None
    company_id: Optional[UUID] = None
    status: str = "wishlist"
    priority: str = "medium"
    probability: int = 50
    notes: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class ApplicationUpdate(BaseModel):
    """Request model for updating application."""

    status: Optional[str] = None
    priority: Optional[str] = None
    probability: Optional[int] = None
    notes: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class ApplicationResponse(BaseModel):
    """Response model for application."""

    id: UUID
    user_id: UUID
    resume_id: UUID
    job_id: Optional[UUID] = None
    company_id: Optional[UUID] = None
    status: str
    stage: Optional[str] = None
    priority: str
    probability: int
    notes: Optional[str] = None
    extra_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Task Models
class TaskCreate(BaseModel):
    """Request model for creating task."""

    application_id: UUID
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"
    task_type: str = "general"


class TaskUpdate(BaseModel):
    """Request model for updating task."""

    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    """Response model for task."""

    id: UUID
    application_id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str
    status: str
    task_type: str
    extra_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Note Models
class NoteCreate(BaseModel):
    """Request model for creating note."""

    application_id: UUID
    content: str
    note_type: str = "general"


class NoteResponse(BaseModel):
    """Response model for note."""

    id: UUID
    application_id: UUID
    user_id: UUID
    content: str
    note_type: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Timeline Event Models
class TimelineEventCreate(BaseModel):
    """Request model for creating timeline event."""

    application_id: UUID
    event_type: str
    title: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    extra_metadata: Optional[dict[str, Any]] = None


class TimelineEventResponse(BaseModel):
    """Response model for timeline event."""

    id: UUID
    application_id: UUID
    event_type: str
    title: str
    description: Optional[str] = None
    event_date: datetime
    extra_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Notification Models
class NotificationCreate(BaseModel):
    """Request model for creating notification."""

    notification_type: str
    title: str
    message: str
    priority: str = "medium"
    application_id: Optional[UUID] = None
    action_url: Optional[str] = None


class NotificationResponse(BaseModel):
    """Response model for notification."""

    id: UUID
    user_id: UUID
    application_id: Optional[UUID] = None
    notification_type: str
    title: str
    message: str
    priority: str
    is_read: bool
    action_url: Optional[str] = None
    extra_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Company Profile Models
class CompanyProfileCreate(BaseModel):
    """Request model for creating company profile."""

    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class CompanyProfileUpdate(BaseModel):
    """Request model for updating company profile."""

    name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class CompanyProfileResponse(BaseModel):
    """Response model for company profile."""

    id: UUID
    user_id: UUID
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    extra_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Workflow Engine Models
class WorkflowTriggerRequest(BaseModel):
    """Request model for triggering workflow."""

    event_type: str
    context: dict[str, Any]


class WorkflowTriggerResponse(BaseModel):
    """Response model for workflow trigger."""

    event_type: str
    actions_executed: int
    results: list[dict[str, Any]]


# Smart Automation Models
class UserActivityData(BaseModel):
    """Model for user activity data."""

    applications: list[dict[str, Any]] = []
    tasks: list[dict[str, Any]] = []
    job_matches: list[dict[str, Any]] = []
    skills: list[str] = []
    job_requirements: list[dict[str, Any]] = []
    last_activity_date: Optional[datetime] = None
    interviews: list[dict[str, Any]] = []
    career_health: dict[str, Any] = {}


class AutomationAnalysisResponse(BaseModel):
    """Response model for automation analysis."""

    total_recommendations: int
    recommendations: list[dict[str, Any]]
    generated_at: datetime


class MorningBriefResponse(BaseModel):
    """Response model for morning brief."""

    greeting: str
    today_priorities: list[dict[str, Any]]
    upcoming_interviews: list[dict[str, Any]]
    deadlines_today: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    career_health: dict[str, Any]


# Dashboard Models
class DashboardMetrics(BaseModel):
    """Dashboard metrics."""

    total_applications: int
    applications_by_stage: dict[str, int]
    pending_tasks: int
    upcoming_interviews: int
    unread_notifications: int
    weekly_progress: dict[str, Any]
    response_rate: float
    interview_rate: float
    offer_rate: float


class DashboardResponse(BaseModel):
    """Response model for dashboard."""

    metrics: DashboardMetrics
    morning_brief: Optional[MorningBriefResponse] = None
    recent_activity: list[dict[str, Any]]
    top_recommendations: list[dict[str, Any]]


# Analytics Models
class AnalyticsMetrics(BaseModel):
    """Analytics metrics."""

    application_funnel: dict[str, int]
    success_rate: float
    response_rate: float
    interview_conversion: float
    offer_conversion: float
    technology_trends: dict[str, int]
    most_successful_resume: Optional[dict[str, Any]]
    most_successful_category: Optional[str]
    most_requested_skills: list[str]
    weak_areas: list[str]


class AnalyticsResponse(BaseModel):
    """Response model for analytics."""

    metrics: AnalyticsMetrics
    generated_at: datetime


# Kanban Models
class KanbanColumn(BaseModel):
    """Kanban column."""

    id: str
    title: str
    status: str
    applications: list[ApplicationResponse]


class KanbanBoardResponse(BaseModel):
    """Response model for kanban board."""

    columns: list[KanbanColumn]


# Career Case Models
class CareerCaseResponse(BaseModel):
    """Response model for career case."""

    application: ApplicationResponse
    resume: dict[str, Any]
    job: dict[str, Any]
    company: Optional[CompanyProfileResponse]
    timeline: list[TimelineEventResponse]
    tasks: list[TaskResponse]
    notes: list[NoteResponse]
    documents: list[dict[str, Any]]
    ai_insights: dict[str, Any]
