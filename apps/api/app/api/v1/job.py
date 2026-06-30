"""Job API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.db.models.job import Job
from app.db.models.user import User
from app.models.job import (
    ATSAnalysisResponse,
    InsightsResponse,
    JobAnalyzeRequest,
    JobAnalyzeResponse,
    JobDetailResponse,
    JobResponse,
    MatchReasoning,
    MissingSkillResponse,
    ResumeJobMatchResponse,
)
from app.repositories.job import JobRepository
from app.repositories.resume import ResumeRepository
from app.services.ats_service import ats_service
from app.services.insights_service import insights_service
from app.services.job_parser import ai_job_parser
from app.services.match_engine import match_engine
from app.services.missing_skills import missing_skills_engine

logger = get_logger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _build_job_response(job) -> JobResponse:
    return JobResponse(
        id=job.id,
        user_id=job.user_id,
        title=job.title,
        company_name=job.company_name,
        department=job.department,
        employment_type=job.employment_type,
        location=job.location,
        remote_status=job.remote_status,
        experience_required=job.experience_required,
        education_required=job.education_required,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        industry=job.industry,
        domain=job.domain,
        seniority=job.seniority,
        raw_description=job.raw_description,
        parsed_data=job.parsed_data,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


def _build_job_detail(job) -> JobDetailResponse:
    return JobDetailResponse(
        job=_build_job_response(job),
        skills=[
            {"name": s.name, "category": s.category, "type": s.type, "importance": s.importance}
            for s in (job.skills or [])
        ],
        requirements=[
            {"requirement": r.requirement, "category": r.category, "is_mandatory": r.is_mandatory}
            for r in (job.requirements or [])
        ],
        responsibilities=[
            {"responsibility": r.responsibility, "priority": r.priority}
            for r in (job.responsibilities or [])
        ],
        benefits=[
            {"benefit": b.benefit, "category": b.category}
            for b in (job.benefits or [])
        ],
        analysis={
            "hiring_signals": job.analysis.hiring_signals,
            "urgency": job.analysis.urgency,
            "leadership_required": job.analysis.leadership_required,
            "communication_level": job.analysis.communication_level,
            "team_size": job.analysis.team_size,
            "growth_potential": job.analysis.growth_potential,
            "work_life_balance": job.analysis.work_life_balance,
            "company_culture_indicators": job.analysis.company_culture_indicators,
            "hidden_expectations": job.analysis.hidden_expectations,
        } if job.analysis else None,
    )


@router.post("/analyze", response_model=JobAnalyzeResponse, status_code=status.HTTP_201_CREATED)
async def analyze_job(
    request: JobAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobAnalyzeResponse:
    """Analyze a job description and match against resume."""
    user_id = str(current_user.id)
    job_repo = JobRepository(db)
    resume_repo = ResumeRepository(db)

    # Load resume
    resume = await resume_repo.get_resume_by_id(request.resume_id)
    if not resume:
        raise NotFoundError("Resume not found")
    if resume.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Parse job with AI
    logger.info(f"Parsing job description for user: {user_id}")
    parsed_job = await ai_job_parser.parse_job(request.job_description)

    # Create job record — use fallbacks for any NULL fields the AI might return
    job = await job_repo.create_job(
        user_id=user_id,
        title=parsed_job.get("title") or "Unknown Role",
        company_name=parsed_job.get("company_name") or "Unknown Company",
        raw_description=request.job_description,
        parsed_data=parsed_job,
        department=parsed_job.get("department"),
        employment_type=parsed_job.get("employment_type"),
        location=parsed_job.get("location"),
        remote_status=parsed_job.get("remote_status"),
        experience_required=parsed_job.get("experience_required"),
        education_required=parsed_job.get("education_required"),
        salary_min=parsed_job.get("salary_min"),
        salary_max=parsed_job.get("salary_max"),
        salary_currency=parsed_job.get("salary_currency"),
        industry=parsed_job.get("industry"),
        domain=parsed_job.get("domain"),
        seniority=parsed_job.get("seniority"),
    )

    # Skills
    skills_data = []
    for skill in parsed_job.get("required_skills", []):
        skills_data.append({"name": skill, "category": "required", "type": "technical"})
    for skill in parsed_job.get("preferred_skills", []):
        skills_data.append({"name": skill, "category": "preferred", "type": "technical"})
    for skill in parsed_job.get("tools", []):
        skills_data.append({"name": skill, "category": "required", "type": "tool"})
    for skill in parsed_job.get("frameworks", []):
        skills_data.append({"name": skill, "category": "required", "type": "framework"})
    for skill in parsed_job.get("programming_languages", []):
        skills_data.append({"name": skill, "category": "required", "type": "language"})
    for skill in parsed_job.get("soft_skills", []):
        skills_data.append({"name": skill, "category": "preferred", "type": "soft"})
    if skills_data:
        await job_repo.create_job_skills(job.id, skills_data)

    # Requirements / responsibilities / benefits
    reqs = [{"requirement": r, "is_mandatory": True} for r in parsed_job.get("requirements", [])]
    if reqs:
        await job_repo.create_job_requirements(job.id, reqs)

    resps = [{"responsibility": r, "priority": i} for i, r in enumerate(parsed_job.get("responsibilities", []))]
    if resps:
        await job_repo.create_job_responsibilities(job.id, resps)

    bens = [{"benefit": b, "category": "general"} for b in parsed_job.get("benefits", [])]
    if bens:
        await job_repo.create_job_benefits(job.id, bens)

    # Job analysis record — guard against nulls from AI
    await job_repo.create_job_analysis(
        job_id=job.id,
        hiring_signals=parsed_job.get("hiring_signals") or [],
        urgency=parsed_job.get("urgency") or "medium",
        leadership_required=bool(parsed_job.get("leadership_required", False)),
        communication_level=parsed_job.get("communication_level") or "intermediate",
        team_size=parsed_job.get("team_size"),
        growth_potential=parsed_job.get("growth_potential") or "medium",
        work_life_balance=parsed_job.get("work_life_balance") or "average",
        company_culture_indicators=parsed_job.get("company_culture_indicators") or [],
        hidden_expectations=parsed_job.get("hidden_expectations") or [],
    )

    # Match calculation
    resume_data = resume.parsed_data or {}
    match_data = match_engine.calculate_match(resume_data, parsed_job)
    match = await job_repo.create_resume_job_match(job.id, request.resume_id, match_data)

    # ATS + missing skills + insights
    ats_data = ats_service.analyze_ats(resume_data, parsed_job)
    await job_repo.create_ats_analysis(match.id, ats_data)

    missing_skills_data = missing_skills_engine.analyze_missing_skills(resume_data, parsed_job)
    await job_repo.create_missing_skills(match.id, missing_skills_data)

    insights_data = await insights_service.generate_insights(resume_data, parsed_job, match_data)

    # Reload job with relationships (use selectinload for async safety)
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(Job)
        .options(
            selectinload(Job.skills),
            selectinload(Job.requirements),
            selectinload(Job.responsibilities),
            selectinload(Job.benefits),
            selectinload(Job.analysis),
        )
        .where(Job.id == job.id)
    )
    job = result.scalar_one()

    return JobAnalyzeResponse(
        job=_build_job_detail(job),
        match=ResumeJobMatchResponse(
            id=match.id,
            job_id=match.job_id,
            resume_id=match.resume_id,
            overall_match=match.overall_match,
            technical_match=match.technical_match,
            experience_match=match.experience_match,
            education_match=match.education_match,
            project_match=match.project_match,
            keyword_match=match.keyword_match,
            ats_match=match.ats_match,
            leadership_match=match.leadership_match,
            communication_match=match.communication_match,
            industry_match=match.industry_match,
            confidence_score=match.confidence_score,
            match_reasoning=MatchReasoning(**match.match_reasoning),
            created_at=match.created_at,
        ),
        missing_skills=[
            MissingSkillResponse(
                skill_name=s.skill_name,
                category=s.category,
                learning_priority=s.learning_priority,
                estimated_learning_time=s.estimated_learning_time,
                difficulty=s.difficulty,
                free_resources=s.free_resources or [],
            )
            for s in (match.missing_skills if hasattr(match, "missing_skills") else [])
        ],
        ats_analysis=ATSAnalysisResponse(
            keyword_coverage=ats_data["keyword_coverage"],
            formatting_compatibility=ats_data["formatting_compatibility"],
            action_verbs_score=ats_data["action_verbs_score"],
            role_alignment=ats_data["role_alignment"],
            missing_keywords=ats_data["missing_keywords"],
            resume_length_score=ats_data["resume_length_score"],
            section_completeness=ats_data["section_completeness"],
            optimization_potential=ats_data["optimization_potential"],
            detailed_report=ats_data["detailed_report"],
        ),
        insights=InsightsResponse(**insights_data),
    )


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[JobResponse]:
    """List all jobs for the current user."""
    user_id = str(current_user.id)
    job_repo = JobRepository(db)
    jobs = await job_repo.get_jobs_by_user(user_id)
    return [_build_job_response(j) for j in jobs]


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobDetailResponse:
    """Get job details by ID."""
    user_id = str(current_user.id)
    result = await db.execute(
        select(Job)
        .options(
            selectinload(Job.skills),
            selectinload(Job.requirements),
            selectinload(Job.responsibilities),
            selectinload(Job.benefits),
            selectinload(Job.analysis),
        )
        .where(Job.id == job_id, Job.is_deleted == False)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise NotFoundError("Job not found")
    if job.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return _build_job_detail(job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a job by ID."""
    user_id = str(current_user.id)
    job_repo = JobRepository(db)
    job = await job_repo.get_job_by_id(job_id)
    if not job:
        raise NotFoundError("Job not found")
    if job.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    await job_repo.delete_job(job_id)
