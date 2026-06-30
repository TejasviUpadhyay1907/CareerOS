"""Application Accelerator API endpoints."""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.logging import get_logger
from app.models.accelerator import (
    CoverLetterGenerateRequest,
    CoverLetterResponse,
    DocumentExportRequest,
    DocumentExportResponse,
    InterviewGenerateRequest,
    InterviewKitResponse,
    RecruiterMessageResponse,
    RecruiterOutreachRequest,
    ResumeOptimizeRequest,
    ResumeOptimizeResponse,
)
from app.models.user import User
from app.repositories.job import JobRepository
from app.repositories.resume import ResumeRepository
from app.services.cover_letter import cover_letter_generator
from app.services.export_engine import export_engine
from app.services.interview_prep import interview_prep_generator
from app.services.recruiter_outreach import recruiter_outreach_generator
from app.services.resume_optimizer import resume_optimizer

logger = get_logger(__name__)

router = APIRouter(prefix="/accelerator", tags=["accelerator"])


@router.post("/optimize/resume", response_model=ResumeOptimizeResponse)
async def optimize_resume(
    request: ResumeOptimizeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumeOptimizeResponse:
    """Optimize resume for a specific job using AI."""
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)

    # Load resume
    resume = await resume_repo.get_resume_by_id(request.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    if resume.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Access denied")

    # Load job
    job = await job_repo.get_job_by_id(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Use raw resume text + parsed data for optimization
    resume_data = resume.parsed_data or {}
    if not resume_data and resume.raw_text:
        resume_data = {"raw_text": resume.raw_text}

    job_data = {
        "title": job.title,
        "company_name": job.company_name,
        "raw_description": job.raw_description,
        **(job.parsed_data or {}),
    }

    # Generate optimization using AI
    optimization = await resume_optimizer.optimize_resume(
        resume_data=resume_data,
        job_data=job_data,
        ats_analysis=None,
        career_intelligence={},
    )

    def _normalize_changes(items: list) -> list:
        """Normalize change items — AI sometimes returns dicts instead of strings."""
        result = []
        for item in (items or []):
            if isinstance(item, dict):
                # Convert nested dicts to readable strings
                original = item.get("original", "")
                optimized = item.get("optimized", "")
                if isinstance(original, dict):
                    original = item.get("name", "") or json.dumps(original)
                if isinstance(optimized, dict):
                    optimized = item.get("name", "") or json.dumps(optimized)
                result.append({
                    "original": str(original),
                    "optimized": str(optimized),
                    "reason": str(item.get("reason", "")),
                    "ats_improvement": str(item.get("ats_improvement", "")),
                    "recruiter_impact": str(item.get("recruiter_impact", "")),
                })
        return result

    def _normalize_skills(skills_data) -> dict:
        if not isinstance(skills_data, dict):
            return {"original_order": [], "optimized_order": [], "reasoning": ""}
        return {
            "original_order": [str(s) for s in (skills_data.get("original_order") or [])],
            "optimized_order": [str(s) for s in (skills_data.get("optimized_order") or [])],
            "reasoning": str(skills_data.get("reasoning") or ""),
        }

    def _normalize_keywords(items: list) -> list:
        result = []
        for item in (items or []):
            if isinstance(item, dict):
                result.append({
                    "keyword": str(item.get("keyword", "")),
                    "where_added": str(item.get("where_added", "")),
                    "reason": str(item.get("reason", "")),
                })
        return result

    return ResumeOptimizeResponse(
        id="opt-" + request.resume_id[:8],
        optimized_summary=str(optimization.get("optimized_summary") or ""),
        optimized_experience=_normalize_changes(optimization.get("optimized_experience")),
        optimized_skills=_normalize_skills(optimization.get("optimized_skills")),
        optimized_projects=_normalize_changes(optimization.get("optimized_projects")),
        keyword_additions=_normalize_keywords(optimization.get("keyword_additions")),
        optimization_score=int(optimization.get("optimization_score") or 0),
        estimated_ats_improvement=int(optimization.get("estimated_ats_improvement") or 0),
        estimated_match_increase=int(optimization.get("estimated_match_increase") or 0),
        estimated_interview_probability=int(optimization.get("estimated_interview_probability") or 0),
        created_at=resume.created_at,
    )


@router.post("/cover-letter/generate", response_model=CoverLetterResponse)
async def generate_cover_letter(
    request: CoverLetterGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CoverLetterResponse:
    """Generate personalized cover letter.

    Generates a cover letter personalized to the company, role,
    resume, and career goals.
    """
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)
    career_repo = CareerRepository(db)
    accelerator_repo = AcceleratorRepository(db)

    # Get resume and job
    resume = await resume_repo.get_resume(request.resume_id)
    job = await job_repo.get_job(request.job_id)

    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get resume analysis
    analysis = await resume_repo.get_latest_analysis(resume.id)
    if not analysis:
        raise HTTPException(status_code=400, detail="Resume must be analyzed first")

    # Get career intelligence
    profile = await career_repo.get_or_create_profile(current_user.id)

    # Prepare data
    resume_data = {
        "name": analysis.name,
        "email": analysis.email,
        "summary": analysis.summary,
        "experience": analysis.experience,
        "skills": analysis.skills,
        "projects": analysis.projects,
    }

    job_data = {
        "title": job.title,
        "company_name": job.company_name,
        "description": job.description,
    }

    career_intelligence = {
        "target_role": profile.target_role,
        "career_goals": [],
    }

    # Generate cover letter
    cover_letter = await cover_letter_generator.generate_cover_letter(
        resume_data=resume_data,
        job_data=job_data,
        career_intelligence=career_intelligence,
        tone=request.tone,
        length=request.length,
    )

    # Store in database
    db_cover_letter = await accelerator_repo.create_cover_letter(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        content=cover_letter["content"],
        tone=cover_letter["tone_used"],
        length=cover_letter["length_used"],
        company_name=cover_letter["company_name"],
        role_title=cover_letter["role_title"],
        personalization_points=cover_letter["personalization_points"],
    )

    return CoverLetterResponse(
        id=str(db_cover_letter.id),
        content=db_cover_letter.content,
        tone=db_cover_letter.tone,
        length=db_cover_letter.length,
        company_name=db_cover_letter.company_name,
        role_title=db_cover_letter.role_title,
        personalization_points=db_cover_letter.personalization_points,
        created_at=db_cover_letter.created_at,
    )


@router.post("/outreach/generate", response_model=RecruiterMessageResponse)
async def generate_outreach(
    request: RecruiterOutreachRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RecruiterMessageResponse:
    """Generate recruiter outreach message.

    Generates personalized outreach messages for various platforms
    and purposes.
    """
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)
    career_repo = CareerRepository(db)
    accelerator_repo = AcceleratorRepository(db)

    # Get resume
    resume = await resume_repo.get_resume(request.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Get job if provided
    job = None
    if request.job_id:
        job = await job_repo.get_job(request.job_id)

    # Get resume analysis
    analysis = await resume_repo.get_latest_analysis(resume.id)
    if not analysis:
        raise HTTPException(status_code=400, detail="Resume must be analyzed first")

    # Get career intelligence
    profile = await career_repo.get_or_create_profile(current_user.id)

    # Prepare data
    resume_data = {
        "name": analysis.name,
        "email": analysis.email,
        "summary": analysis.summary,
        "experience": analysis.experience,
        "skills": analysis.skills,
    }

    job_data = None
    if job:
        job_data = {
            "title": job.title,
            "company_name": job.company_name,
            "description": job.description,
        }

    career_intelligence = {
        "target_role": profile.target_role,
        "career_goals": [],
    }

    # Generate outreach message
    outreach = await recruiter_outreach_generator.generate_outreach(
        resume_data=resume_data,
        job_data=job_data,
        career_intelligence=career_intelligence,
        message_type=request.message_type,
        tone=request.tone,
        length=request.length,
    )

    # Store in database
    db_message = await accelerator_repo.create_recruiter_message(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=request.job_id,
        message_type=outreach["message_type"],
        subject=outreach.get("subject"),
        content=outreach["content"],
        tone=outreach["tone_used"],
        length=outreach["length_used"],
        personalization_reason=outreach["personalization_reason"],
        call_to_action=outreach["call_to_action"],
        recipient_name=None,
        recipient_company=outreach.get("recipient_company"),
        platform="linkedin" if "linkedin" in request.message_type else "email",
    )

    return RecruiterMessageResponse(
        id=str(db_message.id),
        message_type=db_message.message_type,
        subject=db_message.subject,
        content=db_message.content,
        tone=db_message.tone,
        length=db_message.length,
        personalization_reason=db_message.personalization_reason,
        call_to_action=db_message.call_to_action,
        recipient_name=db_message.recipient_name,
        recipient_company=db_message.recipient_company,
        platform=db_message.platform,
        created_at=db_message.created_at,
    )


@router.post("/interview/generate", response_model=InterviewKitResponse)
async def generate_interview_kit(
    request: InterviewGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> InterviewKitResponse:
    """Generate interview preparation kit.

    Generates a comprehensive interview preparation kit including
    questions, topics, and study plans.
    """
    resume_repo = ResumeRepository(db)
    job_repo = JobRepository(db)
    career_repo = CareerRepository(db)
    accelerator_repo = AcceleratorRepository(db)

    # Get resume and job
    resume = await resume_repo.get_resume(request.resume_id)
    job = await job_repo.get_job(request.job_id)

    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get resume analysis
    analysis = await resume_repo.get_latest_analysis(resume.id)
    if not analysis:
        raise HTTPException(status_code=400, detail="Resume must be analyzed first")

    # Get job analysis
    job_analysis = await job_repo.get_job_analysis(job.id)

    # Get career intelligence
    profile = await career_repo.get_or_create_profile(current_user.id)

    # Prepare data
    resume_data = {
        "name": analysis.name,
        "summary": analysis.summary,
        "experience": analysis.experience,
        "skills": analysis.skills,
        "projects": analysis.projects,
    }

    job_data = {
        "title": job.title,
        "company_name": job.company_name,
        "description": job.description,
        "requirements": job_analysis.requirements if job_analysis else [],
        "skills": job_analysis.skills if job_analysis else [],
    }

    ats_analysis = job_analysis.ats_analysis if job_analysis else None

    career_intelligence = {
        "target_role": profile.target_role,
        "career_goals": [],
    }

    # Generate interview kit
    kit = await interview_prep_generator.generate_interview_kit(
        resume_data=resume_data,
        job_data=job_data,
        ats_analysis=ats_analysis,
        career_intelligence=career_intelligence,
    )

    # Store in database
    db_kit = await accelerator_repo.create_interview_kit(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        company_overview=kit.get("company_overview", ""),
        role_overview=kit.get("role_overview", ""),
        responsibilities=kit.get("responsibilities", []),
        technical_topics=kit.get("technical_topics", []),
        behavioral_questions=kit.get("behavioral_questions", []),
        star_suggestions=kit.get("star_suggestions", []),
        project_questions=kit.get("project_questions", []),
        resume_questions=kit.get("resume_questions", []),
        coding_topics=kit.get("coding_topics", []),
        system_design_topics=kit.get("system_design_topics", []),
        hr_questions=kit.get("hr_questions", []),
        salary_tips=kit.get("salary_tips", []),
        questions_to_ask=kit.get("questions_to_ask", []),
        study_plan_90min=kit.get("study_plan_90min", []),
        study_plan_3day=kit.get("study_plan_3day", []),
        study_plan_7day=kit.get("study_plan_7day", []),
        priority_ranking=kit.get("priority_ranking", {}),
    )

    return InterviewKitResponse(
        id=str(db_kit.id),
        company_name=kit.get("company_name", job.company_name),
        role_title=kit.get("role_title", job.title),
        company_overview=db_kit.company_overview,
        role_overview=db_kit.role_overview,
        responsibilities=db_kit.responsibilities,
        technical_topics=db_kit.technical_topics,
        behavioral_questions=db_kit.behavioral_questions,
        project_questions=db_kit.project_questions,
        resume_questions=db_kit.resume_questions,
        coding_topics=db_kit.coding_topics,
        system_design_topics=db_kit.system_design_topics,
        hr_questions=db_kit.hr_questions,
        salary_tips=db_kit.salary_tips,
        questions_to_ask=db_kit.questions_to_ask,
        study_plan_90min=db_kit.study_plan_90min,
        study_plan_3day=db_kit.study_plan_3day,
        study_plan_7day=db_kit.study_plan_7day,
        priority_ranking=db_kit.priority_ranking,
        created_at=db_kit.created_at,
    )


@router.post("/documents/export", response_model=DocumentExportResponse)
async def export_document(
    request: DocumentExportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DocumentExportResponse:
    """Export generated document.

    Exports a document in the specified format.
    """
    accelerator_repo = AcceleratorRepository(db)

    # Get document
    documents = await accelerator_repo.get_generated_documents(current_user.id)
    document = next((d for d in documents if str(d.id) == request.document_id), None)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Export based on format
    if request.format == "markdown":
        file_path = export_engine.export_to_text(
            content=document.description or "",
            title=document.title,
        )
    else:
        file_path = export_engine.export_to_text(
            content=document.description or "",
            title=document.title,
        )

    return DocumentExportResponse(
        file_path=file_path,
        format=request.format,
        file_size=0,
    )
