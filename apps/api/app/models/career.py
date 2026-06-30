"""Pydantic models for career intelligence operations."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# Request Models
class CareerProfileUpdateRequest(BaseModel):
    """Request to update career profile."""

    current_role: Optional[str] = None
    target_role: Optional[str] = None
    target_industry: Optional[str] = None
    target_seniority: Optional[str] = None
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None
    preferred_locations: Optional[list[str]] = None
    remote_preference: Optional[str] = None
    work_style: Optional[str] = None
    career_stage: Optional[str] = None
    years_experience: Optional[int] = None
    primary_domain: Optional[str] = None
    secondary_domains: Optional[list[str]] = None
    career_focus_areas: Optional[list[str]] = None
    learning_style: Optional[str] = None
    risk_tolerance: Optional[str] = None
    growth_priority: Optional[str] = None
    work_life_balance_priority: Optional[str] = None
    company_size_preference: Optional[str] = None
    company_type_preference: Optional[str] = None
    additional_preferences: Optional[dict[str, Any]] = None


class CareerGoalRequest(BaseModel):
    """Request to create career goal."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    target_date: Optional[str] = None
    priority: str = Field(..., min_length=1, max_length=50)


class RecommendationFeedbackRequest(BaseModel):
    """Request to provide feedback on recommendation."""

    status: str = Field(..., min_length=1, max_length=50)
    user_status: str = Field(..., min_length=1, max_length=50)
    feedback: Optional[str] = None


# Response Models
class HealthBreakdownItem(BaseModel):
    """Health score breakdown item."""

    score: int
    weight: int
    reasoning: str


class HealthScoreResponse(BaseModel):
    """Career health score response."""

    overall_score: int
    breakdown: dict[str, HealthBreakdownItem]
    grade: str
    trend: str


class InsightResponse(BaseModel):
    """Career insight response."""

    id: str
    type: str
    title: str
    description: str
    category: str
    severity: str
    confidence: float
    evidence: list[str]
    actionable: bool
    created_at: datetime


class RecommendationResponse(BaseModel):
    """Career recommendation response."""

    id: str
    title: str
    description: str
    category: str
    priority: str
    difficulty: str
    estimated_time: str
    expected_benefit: str
    confidence: float
    evidence: list[str]
    status: str
    user_status: str
    completed_at: Optional[datetime]
    created_at: datetime


class PredictionResponse(BaseModel):
    """Career prediction response."""

    id: str
    type: str
    title: str
    description: str
    predicted_value: float
    confidence: float
    time_horizon: str
    factors: list[str]
    created_at: datetime


class OpportunityResponse(BaseModel):
    """Career opportunity response."""

    type: str
    title: str
    description: str
    confidence: float
    evidence: list[str]


class CareerGoalResponse(BaseModel):
    """Career goal response."""

    id: str
    title: str
    description: Optional[str]
    category: str
    target_date: Optional[str]
    status: str
    priority: str
    progress: int
    created_at: datetime


class CareerProfileResponse(BaseModel):
    """Career profile response."""

    id: str
    user_id: str
    current_role: Optional[str]
    target_role: Optional[str]
    target_industry: Optional[str]
    target_seniority: Optional[str]
    salary_expectation_min: Optional[int]
    salary_expectation_max: Optional[int]
    preferred_locations: Optional[list[str]]
    remote_preference: Optional[str]
    work_style: Optional[str]
    career_stage: Optional[str]
    years_experience: Optional[int]
    primary_domain: Optional[str]
    secondary_domains: Optional[list[str]]
    career_focus_areas: Optional[list[str]]
    learning_style: Optional[str]
    risk_tolerance: Optional[str]
    growth_priority: Optional[str]
    work_life_balance_priority: Optional[str]
    company_size_preference: Optional[str]
    company_type_preference: Optional[str]
    created_at: datetime
    updated_at: datetime


class TodayPriorityItem(BaseModel):
    """Today's priority item."""

    title: str
    description: str
    estimated_time: str
    expected_benefit: str
    confidence: float


class DashboardResponse(BaseModel):
    """Career dashboard response."""

    greeting: str
    health_score: HealthScoreResponse
    todays_priorities: list[TodayPriorityItem]
    insights: list[InsightResponse]
    recommendations: list[RecommendationResponse]
    predictions: list[PredictionResponse]
    opportunities: list[OpportunityResponse]
    goals: list[CareerGoalResponse]
    profile: CareerProfileResponse


class RecommendationUpdateResponse(BaseModel):
    """Response for recommendation update."""

    id: str
    status: str
    user_status: str
    feedback: Optional[str]
    completed_at: Optional[datetime]
