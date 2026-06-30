"""Career Intelligence Engine database models — SQLite/PostgreSQL compatible."""
import uuid as _uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def _new_uuid() -> str:
    return str(_uuid.uuid4())


class CareerProfile(Base, TimestampMixin):
    __tablename__ = "career_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    current_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_industry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_seniority: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    salary_expectation_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_expectation_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    preferred_locations: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    remote_preference: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    work_style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    career_stage: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    years_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    primary_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    secondary_domains: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    career_focus_areas: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    learning_style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    risk_tolerance: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    growth_priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    work_life_balance_priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_size_preference: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_type_preference: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    additional_preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    goals = relationship("CareerGoal", back_populates="profile", cascade="all, delete-orphan")
    insights = relationship("CareerInsight", back_populates="profile", cascade="all, delete-orphan")


class CareerGoal(Base, TimestampMixin):
    __tablename__ = "career_goals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    milestones: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    metrics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile = relationship("CareerProfile", back_populates="goals")


class CareerInsight(Base, TimestampMixin):
    __tablename__ = "career_insights"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    insight_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    severity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    evidence: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    related_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_actionable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile = relationship("CareerProfile", back_populates="insights")
    recommendations = relationship("CareerRecommendation", back_populates="insight", cascade="all, delete-orphan")


class CareerRecommendation(Base, TimestampMixin):
    __tablename__ = "career_recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    insight_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("career_insights.id"), nullable=True, index=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    time_horizon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    estimated_time: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    expected_benefit: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dependencies: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    evidence: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    user_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    effectiveness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    insight = relationship("CareerInsight", back_populates="recommendations")


class CareerPrediction(Base, TimestampMixin):
    __tablename__ = "career_predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    prediction_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    predicted_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    time_horizon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    factors: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    historical_accuracy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CareerAction(Base, TimestampMixin):
    __tablename__ = "career_actions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    action_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class DailyAIReport(Base, TimestampMixin):
    __tablename__ = "daily_ai_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    career_health_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    health_breakdown: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    top_priorities: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    key_insights: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    recommendations: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    predictions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class WeeklyAIReport(Base, TimestampMixin):
    __tablename__ = "weekly_ai_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    week_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    week_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    career_health_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    health_trend: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    weekly_progress: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    achievements: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    areas_for_improvement: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    trend_analysis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    forecast: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AdvisorMemory(Base, TimestampMixin):
    __tablename__ = "advisor_memory"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    memory_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    value: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_accessed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    access_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AdvisorFeedback(Base, TimestampMixin):
    __tablename__ = "advisor_feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("career_profiles.id"), nullable=False, index=True)
    recommendation_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("career_recommendations.id"), nullable=True)
    feedback_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    helpful: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    implemented: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
