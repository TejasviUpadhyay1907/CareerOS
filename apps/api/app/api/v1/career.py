"""Career Intelligence API endpoints."""
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.logging import get_logger
from app.models.career import (
    CareerGoalRequest,
    CareerProfileResponse,
    CareerProfileUpdateRequest,
    DashboardResponse,
    HealthScoreResponse,
    RecommendationFeedbackRequest,
    RecommendationUpdateResponse,
)
from app.models.user import User
from app.repositories.career import CareerRepository
from app.repositories.job import JobRepository
from app.repositories.resume import ResumeRepository
from app.services.career_health import career_health_service
from app.services.career_reasoning import career_reasoning_engine

logger = get_logger(__name__)

router = APIRouter(prefix="/career", tags=["career"])


@router.get("/dashboard", response_model=DashboardResponse)
async def get_career_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardResponse:
    """Get career intelligence dashboard.

    Returns comprehensive career intelligence including health score,
    insights, recommendations, predictions, and today's priorities.
    """
    career_repo = CareerRepository(db)
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)

    # Get or create profile
    profile = await career_repo.get_or_create_profile(current_user.id)

    # Get user's resume data
    resumes = await resume_repo.get_resumes_by_user(current_user.id)
    resume_data = None
    if resumes:
        resume = resumes[0]
        analysis = await resume_repo.get_latest_analysis(resume.id)
        if analysis:
            resume_data = {
                "experience": analysis.experience,
                "education": analysis.education,
                "skills": analysis.skills,
                "projects": analysis.projects,
                "achievements": analysis.achievements,
                "years_of_experience": analysis.years_of_experience,
                "primary_domain": analysis.primary_domain,
            }

    # Get job match data
    job_matches = await job_repo.get_job_matches_by_user(current_user.id)
    job_data = []
    for match in job_matches:
        job = await job_repo.get_job(match.job_id)
        if job:
            job_data.append({
                "job_title": job.title,
                "company_name": job.company_name,
                "overall_match": match.overall_match,
                "ats_match": match.ats_match,
                "technical_match": match.technical_match,
            })

    # Get application activity (simplified for now)
    application_data = {
        "recent_applications_count": len(job_data),
        "days_since_last_application": 5 if job_data else 30,
        "response_rate": 0.15,
    }

    # Get career goals
    goals = []
    # Would fetch from database when goal repository is implemented

    # Generate career intelligence
    career_data = {
        "profile_id": str(profile.id),
        "current_role": profile.current_role,
        "target_role": profile.target_role,
        "target_industry": profile.target_industry,
        "years_experience": profile.years_experience,
        "primary_domain": profile.primary_domain,
        "goals": goals,
    }

    try:
        intelligence = await career_reasoning_engine.generate_career_intelligence(
            career_data=career_data,
            resume_data=resume_data,
            job_data=job_data,
            application_data=application_data,
        )
    except Exception as e:
        logger.error(f"Failed to generate career intelligence: {e}")
        # Fallback to health score only
        intelligence = {
            "insights": [],
            "recommendations": [],
            "predictions": [],
            "opportunities": [],
            "health_score": career_health_service.calculate_health_score(
                resume_data=resume_data,
                job_matches=job_data,
                application_activity=application_data,
                career_goals=goals,
            ),
        }

    # Generate today's priorities
    todays_priorities = career_reasoning_engine.generate_todays_priorities(
        intelligence.get("recommendations", []),
        intelligence.get("health_score", {}),
    )

    # Store insights and recommendations in database
    for insight_data in intelligence.get("insights", []):
        await career_repo.create_insight(
            profile_id=profile.id,
            insight_type=insight_data["type"],
            title=insight_data["title"],
            description=insight_data["description"],
            category=insight_data["category"],
            severity=insight_data["severity"],
            confidence=insight_data["confidence"],
            evidence=insight_data["evidence"],
            related_data=insight_data.get("related_data", {}),
        )

    for rec_data in intelligence.get("recommendations", []):
        await career_repo.create_recommendation(
            profile_id=profile.id,
            insight_id=None,
            title=rec_data["title"],
            description=rec_data["description"],
            category=rec_data["category"],
            priority=rec_data["priority"],
            difficulty=rec_data["difficulty"],
            estimated_time=rec_data["estimated_time"],
            expected_benefit=rec_data["expected_benefit"],
            confidence=rec_data["confidence"],
            evidence=rec_data["evidence"],
        )

    # Get stored recommendations
    recommendations = await career_repo.get_recommendations(profile.id, status="pending")

    # Generate greeting
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return DashboardResponse(
        greeting=f"{greeting}, {current_user.email.split('@')[0]}",
        health_score=HealthScoreResponse(**intelligence["health_score"]),
        todays_priorities=todays_priorities,
        insights=[],  # Would fetch from database
        recommendations=[
            RecommendationResponse(
                id=str(rec.id),
                title=rec.title,
                description=rec.description,
                category=rec.category,
                priority=rec.priority,
                difficulty=rec.difficulty,
                estimated_time=rec.estimated_time,
                expected_benefit=rec.expected_benefit,
                confidence=rec.confidence,
                evidence=rec.evidence,
                status=rec.status,
                user_status=rec.user_status,
                completed_at=rec.completed_at,
                created_at=rec.created_at,
            )
            for rec in recommendations[:10]
        ],
        predictions=[],  # Would fetch from database
        opportunities=intelligence.get("opportunities", []),
        goals=[],  # Would fetch from database
        profile=CareerProfileResponse(
            id=str(profile.id),
            user_id=str(profile.user_id),
            current_role=profile.current_role,
            target_role=profile.target_role,
            target_industry=profile.target_industry,
            target_seniority=profile.target_seniority,
            salary_expectation_min=profile.salary_expectation_min,
            salary_expectation_max=profile.salary_expectation_max,
            preferred_locations=profile.preferred_locations,
            remote_preference=profile.remote_preference,
            work_style=profile.work_style,
            career_stage=profile.career_stage,
            years_experience=profile.years_experience,
            primary_domain=profile.primary_domain,
            secondary_domains=profile.secondary_domains,
            career_focus_areas=profile.career_focus_areas,
            learning_style=profile.learning_style,
            risk_tolerance=profile.risk_tolerance,
            growth_priority=profile.growth_priority,
            work_life_balance_priority=profile.work_life_balance_priority,
            company_size_preference=profile.company_size_preference,
            company_type_preference=profile.company_type_preference,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        ),
    )


@router.get("/health", response_model=HealthScoreResponse)
async def get_career_health(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> HealthScoreResponse:
    """Get career health score.

    Returns detailed health score with breakdown across multiple dimensions.
    """
    career_repo = CareerRepository(db)
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)

    # Get profile
    profile = await career_repo.get_or_create_profile(current_user.id)

    # Get resume data
    resumes = await resume_repo.get_resumes_by_user(current_user.id)
    resume_data = None
    if resumes:
        resume = resumes[0]
        analysis = await resume_repo.get_latest_analysis(resume.id)
        if analysis:
            resume_data = {
                "experience": analysis.experience,
                "education": analysis.education,
                "skills": analysis.skills,
                "projects": analysis.projects,
                "achievements": analysis.achievements,
                "years_of_experience": analysis.years_of_experience,
                "primary_domain": analysis.primary_domain,
            }

    # Get job match data
    job_matches = await job_repo.get_job_matches_by_user(current_user.id)
    job_data = []
    for match in job_matches:
        job = await job_repo.get_job(match.job_id)
        if job:
            job_data.append({
                "job_title": job.title,
                "company_name": job.company_name,
                "overall_match": match.overall_match,
                "ats_match": match.ats_match,
                "technical_match": match.technical_match,
            })

    # Calculate health score
    health_score = career_health_service.calculate_health_score(
        resume_data=resume_data,
        job_matches=job_data,
        application_activity={
            "recent_applications_count": len(job_data),
            "days_since_last_application": 5 if job_data else 30,
            "response_rate": 0.15,
        },
        career_goals=[],
    )

    return HealthScoreResponse(**health_score)


@router.patch("/profile", response_model=CareerProfileResponse)
async def update_career_profile(
    profile_update: CareerProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CareerProfileResponse:
    """Update career profile.

    Allows user to update their career preferences and goals.
    """
    career_repo = CareerRepository(db)

    profile = await career_repo.get_or_create_profile(current_user.id)

    update_data = profile_update.model_dump(exclude_unset=True)
    updated_profile = await career_repo.update_profile(profile.id, **update_data)

    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return CareerProfileResponse(
        id=str(updated_profile.id),
        user_id=str(updated_profile.user_id),
        current_role=updated_profile.current_role,
        target_role=updated_profile.target_role,
        target_industry=updated_profile.target_industry,
        target_seniority=updated_profile.target_seniority,
        salary_expectation_min=updated_profile.salary_expectation_min,
        salary_expectation_max=updated_profile.salary_expectation_max,
        preferred_locations=updated_profile.preferred_locations,
        remote_preference=updated_profile.remote_preference,
        work_style=updated_profile.work_style,
        career_stage=updated_profile.career_stage,
        years_experience=updated_profile.years_experience,
        primary_domain=updated_profile.primary_domain,
        secondary_domains=updated_profile.secondary_domains,
        career_focus_areas=updated_profile.career_focus_areas,
        learning_style=updated_profile.learning_style,
        risk_tolerance=updated_profile.risk_tolerance,
        growth_priority=updated_profile.growth_priority,
        work_life_balance_priority=updated_profile.work_life_balance_priority,
        company_size_preference=updated_profile.company_size_preference,
        company_type_preference=updated_profile.company_type_preference,
        created_at=updated_profile.created_at,
        updated_at=updated_profile.updated_at,
    )


@router.post("/goals")
async def create_career_goal(
    goal_request: CareerGoalRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Create a career goal.

    Allows user to set career goals for tracking and alignment.
    """
    career_repo = CareerRepository(db)

    profile = await career_repo.get_or_create_profile(current_user.id)

    goal = await career_repo.create_goal(
        profile_id=profile.id,
        title=goal_request.title,
        description=goal_request.description,
        category=goal_request.category,
        target_date=goal_request.target_date,
        priority=goal_request.priority,
    )

    return {"id": str(goal.id), "message": "Goal created successfully"}


@router.patch("/recommendations/{recommendation_id}", response_model=RecommendationUpdateResponse)
async def update_recommendation(
    recommendation_id: str,
    feedback: RecommendationFeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RecommendationUpdateResponse:
    """Update recommendation status and provide feedback.

    Allows user to mark recommendations as completed/ignored and provide feedback.
    """
    career_repo = CareerRepository(db)

    profile = await career_repo.get_or_create_profile(current_user.id)

    updated = await career_repo.update_recommendation_status(
        recommendation_id=recommendation_id,
        status=feedback.status,
        user_status=feedback.user_status,
        feedback=feedback.feedback,
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    # Record feedback
    if feedback.feedback:
        await career_repo.record_feedback(
            profile_id=profile.id,
            recommendation_id=recommendation_id,
            feedback_type="recommendation_feedback",
            rating=None,
            comment=feedback.feedback,
            helpful=None,
            implemented=None,
        )

    return RecommendationUpdateResponse(
        id=str(updated.id),
        status=updated.status,
        user_status=updated.user_status,
        feedback=updated.feedback,
        completed_at=updated.completed_at,
    )


# ---------------------------------------------------------------------------
# Career Advisor Chat
# ---------------------------------------------------------------------------
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: str = ""


@router.post("/chat")
async def career_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """AI career advisor chat endpoint."""
    from app.ai.openai_client import openai_client
    from datetime import datetime

    await openai_client.initialize()

    current_date = datetime.utcnow().strftime("%B %d, %Y")

    system_prompt = (
        f"You are an expert AI Career Advisor for CareerOS. Today's date is {current_date}.\n"
        "You help users with resume improvement, job searching, interview preparation, "
        "salary negotiation, career transitions, and skill development.\n"
        "IMPORTANT RULES:\n"
        "- Always give advice relevant to 2025-2026 job market trends and technologies.\n"
        "- Be specific, actionable, and personalized. Never give generic advice.\n"
        "- Format your response as plain readable text — NO markdown symbols like **, ##, or *.\n"
        "- Use numbered lists (1. 2. 3.) or dashes (-) for bullet points.\n"
        "- Keep responses concise and well-structured with clear sections.\n"
        "- Always reference the user's context when available.\n\n"
        "User context:\n" + request.context
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in request.messages[-20:]:  # last 20 messages for context window
        messages.append({"role": msg.role, "content": msg.content})

    try:
        reply = await openai_client.chat_completion(
            messages=messages,
            model="openai/gpt-4o-mini",  # OpenRouter format
            temperature=0.7,
        )
        return {"reply": reply}
    except Exception as e:
        logger.error(f"Career chat error: {e}", exc_info=True)
        # Return the actual error for debugging
        return {
            "reply": f"AI Error: {str(e)}. Check backend logs for details."
        }
