"""Repository layer for career intelligence data access."""
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    AdvisorFeedback,
    AdvisorMemory,
    CareerAction,
    CareerGoal,
    CareerInsight,
    CareerPrediction,
    CareerProfile,
    CareerRecommendation,
    DailyAIReport,
    WeeklyAIReport,
)

logger = get_logger(__name__)


class CareerRepository:
    """Repository for career intelligence operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    async def get_or_create_profile(self, user_id: str) -> CareerProfile:
        """Get or create career profile for user.

        Args:
            user_id: User ID

        Returns:
            Career profile
        """
        result = await self.db.execute(
            select(CareerProfile).where(
                CareerProfile.user_id == user_id, CareerProfile.is_deleted == False
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            profile = CareerProfile(user_id=user_id)
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
            logger.info(f"Created career profile for user: {user_id}")

        return profile

    async def update_profile(
        self, profile_id: str, **kwargs
    ) -> Optional[CareerProfile]:
        """Update career profile.

        Args:
            profile_id: Profile ID
            **kwargs: Fields to update

        Returns:
            Updated profile or None
        """
        result = await self.db.execute(
            select(CareerProfile).where(
                CareerProfile.id == profile_id, CareerProfile.is_deleted == False
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(f"Updated career profile: {profile_id}")
        return profile

    async def create_insight(
        self,
        profile_id: str,
        insight_type: str,
        title: str,
        description: str,
        category: str,
        severity: str,
        confidence: float,
        evidence: list[str],
        related_data: Optional[dict[str, Any]] = None,
    ) -> CareerInsight:
        """Create career insight.

        Args:
            profile_id: Profile ID
            insight_type: Type of insight
            title: Insight title
            description: Insight description
            category: Insight category
            severity: Insight severity
            confidence: Confidence score
            evidence: Supporting evidence
            related_data: Related data

        Returns:
            Created insight
        """
        insight = CareerInsight(
            profile_id=profile_id,
            insight_type=insight_type,
            title=title,
            description=description,
            category=category,
            severity=severity,
            confidence=confidence,
            evidence=evidence,
            related_data=related_data or {},
            is_actionable=True,
        )

        self.db.add(insight)
        await self.db.commit()
        await self.db.refresh(insight)

        logger.info(f"Created career insight: {insight.id}")
        return insight

    async def create_recommendation(
        self,
        profile_id: str,
        insight_id: Optional[str],
        title: str,
        description: str,
        category: str,
        priority: str,
        difficulty: str,
        estimated_time: str,
        expected_benefit: str,
        confidence: float,
        evidence: list[str],
    ) -> CareerRecommendation:
        """Create career recommendation.

        Args:
            profile_id: Profile ID
            insight_id: Related insight ID
            title: Recommendation title
            description: Recommendation description
            category: Time horizon category
            priority: Priority level
            difficulty: Difficulty level
            estimated_time: Estimated time
            expected_benefit: Expected benefit
            confidence: Confidence score
            evidence: Supporting evidence

        Returns:
            Created recommendation
        """
        recommendation = CareerRecommendation(
            profile_id=profile_id,
            insight_id=insight_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            difficulty=difficulty,
            estimated_time=estimated_time,
            expected_benefit=expected_benefit,
            confidence=confidence,
            evidence=evidence,
            status="pending",
            user_status="pending",
        )

        self.db.add(recommendation)
        await self.db.commit()
        await self.db.refresh(recommendation)

        logger.info(f"Created career recommendation: {recommendation.id}")
        return recommendation

    async def create_prediction(
        self,
        profile_id: str,
        prediction_type: str,
        title: str,
        description: str,
        predicted_value: float,
        confidence: float,
        time_horizon: str,
        factors: list[str],
    ) -> CareerPrediction:
        """Create career prediction.

        Args:
            profile_id: Profile ID
            prediction_type: Type of prediction
            title: Prediction title
            description: Prediction description
            predicted_value: Predicted value
            confidence: Confidence score
            time_horizon: Time horizon
            factors: Contributing factors

        Returns:
            Created prediction
        """
        prediction = CareerPrediction(
            profile_id=profile_id,
            prediction_type=prediction_type,
            title=title,
            description=description,
            predicted_value=predicted_value,
            confidence=confidence,
            time_horizon=time_horizon,
            factors=factors,
        )

        self.db.add(prediction)
        await self.db.commit()
        await self.db.refresh(prediction)

        logger.info(f"Created career prediction: {prediction.id}")
        return prediction

    async def create_goal(
        self,
        profile_id: str,
        title: str,
        description: Optional[str],
        category: str,
        target_date: Optional[str],
        priority: str,
    ) -> CareerGoal:
        """Create career goal.

        Args:
            profile_id: Profile ID
            title: Goal title
            description: Goal description
            category: Goal category
            target_date: Target date
            priority: Priority level

        Returns:
            Created goal
        """
        goal = CareerGoal(
            profile_id=profile_id,
            title=title,
            description=description,
            category=category,
            target_date=target_date,
            status="active",
            priority=priority,
            progress=0,
        )

        self.db.add(goal)
        await self.db.commit()
        await self.db.refresh(goal)

        logger.info(f"Created career goal: {goal.id}")
        return goal

    async def create_daily_report(
        self,
        profile_id: str,
        report_date: str,
        career_health_score: int,
        health_breakdown: dict[str, Any],
        top_priorities: list[dict[str, Any]],
        key_insights: list[dict[str, Any]],
        recommendations: list[dict[str, Any]],
        predictions: list[dict[str, Any]],
    ) -> DailyAIReport:
        """Create daily AI report.

        Args:
            profile_id: Profile ID
            report_date: Report date
            career_health_score: Health score
            health_breakdown: Health score breakdown
            top_priorities: Top priorities
            key_insights: Key insights
            recommendations: Recommendations
            predictions: Predictions

        Returns:
            Created daily report
        """
        report = DailyAIReport(
            profile_id=profile_id,
            report_date=report_date,
            career_health_score=career_health_score,
            health_breakdown=health_breakdown,
            top_priorities=top_priorities,
            key_insights=key_insights,
            recommendations=recommendations,
            predictions=predictions,
        )

        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)

        logger.info(f"Created daily AI report: {report.id}")
        return report

    async def get_latest_daily_report(self, profile_id: str) -> Optional[DailyAIReport]:
        """Get latest daily report for profile.

        Args:
            profile_id: Profile ID

        Returns:
            Latest daily report or None
        """
        result = await self.db.execute(
            select(DailyAIReport)
            .where(DailyAIReport.profile_id == profile_id, DailyAIReport.is_deleted == False)
            .order_by(DailyAIReport.report_date.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_recommendations(
        self, profile_id: str, status: Optional[str] = None
    ) -> list[CareerRecommendation]:
        """Get recommendations for profile.

        Args:
            profile_id: Profile ID
            status: Filter by status

        Returns:
            List of recommendations
        """
        query = select(CareerRecommendation).where(
            CareerRecommendation.profile_id == profile_id, CareerRecommendation.is_deleted == False
        )

        if status:
            query = query.where(CareerRecommendation.status == status)

        query = query.order_by(CareerRecommendation.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_recommendation_status(
        self, recommendation_id: str, status: str, user_status: str, feedback: Optional[str] = None
    ) -> Optional[CareerRecommendation]:
        """Update recommendation status.

        Args:
            recommendation_id: Recommendation ID
            status: System status
            user_status: User status
            feedback: User feedback

        Returns:
            Updated recommendation or None
        """
        result = await self.db.execute(
            select(CareerRecommendation).where(
                CareerRecommendation.id == recommendation_id, CareerRecommendation.is_deleted == False
            )
        )
        recommendation = result.scalar_one_or_none()

        if not recommendation:
            return None

        recommendation.status = status
        recommendation.user_status = user_status
        if feedback:
            recommendation.feedback = feedback

        if status == "completed":
            from datetime import datetime
            recommendation.completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(recommendation)

        logger.info(f"Updated recommendation status: {recommendation_id}")
        return recommendation

    async def store_memory(
        self, profile_id: str, memory_type: str, key: str, value: Any, context: Optional[str] = None
    ) -> AdvisorMemory:
        """Store advisor memory.

        Args:
            profile_id: Profile ID
            memory_type: Type of memory
            key: Memory key
            value: Memory value
            context: Context

        Returns:
            Created memory
        """
        memory = AdvisorMemory(
            profile_id=profile_id,
            memory_type=memory_type,
            key=key,
            value=value,
            context=context,
            confidence=0.8,
            access_count=0,
        )

        self.db.add(memory)
        await self.db.commit()
        await self.db.refresh(memory)

        logger.info(f"Stored advisor memory: {memory.id}")
        return memory

    async def get_memory(
        self, profile_id: str, memory_type: Optional[str] = None, key: Optional[str] = None
    ) -> list[AdvisorMemory]:
        """Get advisor memories.

        Args:
            profile_id: Profile ID
            memory_type: Filter by type
            key: Filter by key

        Returns:
            List of memories
        """
        query = select(AdvisorMemory).where(
            AdvisorMemory.profile_id == profile_id, AdvisorMemory.is_deleted == False
        )

        if memory_type:
            query = query.where(AdvisorMemory.memory_type == memory_type)
        if key:
            query = query.where(AdvisorMemory.key == key)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def record_feedback(
        self,
        profile_id: str,
        recommendation_id: Optional[str],
        feedback_type: str,
        rating: Optional[int],
        comment: Optional[str],
        helpful: Optional[bool],
        implemented: Optional[bool],
    ) -> AdvisorFeedback:
        """Record user feedback.

        Args:
            profile_id: Profile ID
            recommendation_id: Related recommendation ID
            feedback_type: Type of feedback
            rating: Rating
            comment: Comment
            helpful: Was it helpful
            implemented: Was it implemented

        Returns:
            Created feedback
        """
        feedback = AdvisorFeedback(
            profile_id=profile_id,
            recommendation_id=recommendation_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            helpful=helpful,
            implemented=implemented,
        )

        self.db.add(feedback)
        await self.db.commit()
        await self.db.refresh(feedback)

        logger.info(f"Recorded advisor feedback: {feedback.id}")
        return feedback
