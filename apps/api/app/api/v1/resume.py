"""Resume API endpoints."""
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.exceptions import NotFoundError, ValidationError
from app.core.logging import get_logger
from app.db.models.user import User
from app.db.session import get_db
from app.models.resume import (
    ResumeAnalyzeRequest,
    ResumeAnalyzeResponse,
    ResumeAnalysisResponse,
    ResumeDetailResponse,
    ResumeMetadataResponse,
    ResumeResponse,
    ResumeSummaryRequest,
    ResumeSummaryResponse,
    ResumeUploadRequest,
    ResumeUploadResponse,
)
from app.repositories.resume import ResumeRepository
from app.services.ai_parser import ai_resume_parser
from app.services.health_score import health_score_service
from app.services.parser import parser_service
from app.services.storage import storage_service
from app.services.summary import summary_service

logger = get_logger(__name__)

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumeUploadResponse:
    """Upload a resume file."""
    # Validate that user can only upload for themselves
    if user_id != str(current_user.id):
        raise ValidationError("You can only upload resumes for yourself")
    
    # Validate file
    if not file.filename:
        raise ValidationError("Filename is required")

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Validate file size (10MB max)
    if file_size > 10 * 1024 * 1024:
        raise ValidationError("File size exceeds 10MB limit")

    # Validate MIME type (temporarily allow text for testing)
    mime_type = file.content_type or "application/octet-stream"
    allowed_types = [
        "application/pdf", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"  # Temporary for testing
    ]
    if mime_type not in allowed_types:
        raise ValidationError(f"Invalid file type: {mime_type}. Only PDF, DOCX, and text files are supported")

    try:
        # Initialize storage service
        await storage_service.initialize()

        # Upload to storage
        storage_path, storage_url = await storage_service.upload_file(
            file_content=file_content,
            original_filename=file.filename,
            user_id=user_id,
            mime_type=mime_type,
        )

        # Extract text
        if mime_type == "application/pdf":
            raw_text = await parser_service.extract_text_from_pdf(file_content)
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            raw_text = await parser_service.extract_text_from_docx(file_content)
        else:
            # For text files, use content directly (temporary testing)
            raw_text = file_content.decode('utf-8', errors='ignore')

        # Create resume record
        repo = ResumeRepository(db)
        resume = await repo.create_resume(
            user_id=user_id,
            original_filename=file.filename,
            storage_path=storage_path,
            storage_url=storage_url,
            file_size=file_size,
            mime_type=mime_type,
            raw_text=raw_text,
        )

        logger.info(f"Resume uploaded successfully: {resume.id}")
        return ResumeUploadResponse(
            id=str(resume.id),
            original_filename=resume.original_filename,
            storage_url=resume.storage_url,
            file_size=resume.file_size,
            mime_type=resume.mime_type,
            created_at=resume.created_at,
        )

    except Exception as e:
        logger.error(f"Failed to upload resume: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ResumeResponse]:
    """List all resumes for a user."""
    # Validate that user can only access their own resumes
    if user_id != str(current_user.id):
        raise ValidationError("You can only access your own resumes")
    
    repo = ResumeRepository(db)
    resumes = await repo.get_resumes_by_user(user_id)

    return [
        ResumeResponse(
            id=str(resume.id),
            user_id=resume.user_id,
            original_filename=resume.original_filename,
            storage_url=resume.storage_url,
            file_size=resume.file_size,
            mime_type=resume.mime_type,
            is_primary=resume.is_primary,
            raw_text=resume.raw_text,
            parsed_data=resume.parsed_data,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        )
        for resume in resumes
    ]


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumeDetailResponse:
    """Get a resume by ID with all related data."""
    repo = ResumeRepository(db)
    resume = await repo.get_resume_by_id(resume_id)

    if not resume:
        raise NotFoundError("Resume not found")

    # Build response
    return ResumeDetailResponse(
        resume=ResumeResponse(
            id=str(resume.id),
            user_id=resume.user_id,
            original_filename=resume.original_filename,
            storage_url=resume.storage_url,
            file_size=resume.file_size,
            mime_type=resume.mime_type,
            is_primary=resume.is_primary,
            raw_text=resume.raw_text,
            parsed_data=resume.parsed_data,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
        ),
        metadata=None,  # Will be populated when analysis is run
        analysis=None,  # Will be populated when analysis is run
        skills=[],
        experience=[],
        education=[],
        projects=[],
        certifications=[],
        languages=[],
        achievements=[],
        links=[],
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a resume."""
    repo = ResumeRepository(db)
    deleted = await repo.delete_resume(resume_id)

    if not deleted:
        raise NotFoundError("Resume not found")

    logger.info(f"Resume deleted: {resume_id}")


@router.post("/analyze", response_model=ResumeAnalyzeResponse)
async def analyze_resume(
    request: ResumeAnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumeAnalyzeResponse:
    """Analyze a resume using AI."""
    repo = ResumeRepository(db)
    resume = await repo.get_resume_by_id(request.resume_id)

    if not resume:
        raise NotFoundError("Resume not found")

    if not resume.raw_text:
        # Use filename as fallback text so at least basic analysis works
        fallback = f"Resume: {resume.original_filename}. No extractable text found."
        await repo.update_resume(request.resume_id, raw_text=fallback)
        resume.raw_text = fallback

    try:
        # Parse resume with AI
        parsed_data = await ai_resume_parser.parse_resume(resume.raw_text)

        # Update resume with parsed data
        await repo.update_resume(request.resume_id, parsed_data=parsed_data)

        # Calculate health score
        health_result = health_score_service.calculate_health_score(parsed_data)
        # Create or update analysis record (upsert)
        existing_analysis = await repo.get_analysis_by_resume(request.resume_id)
        if existing_analysis:
            await repo.update_analysis(
                resume_id=request.resume_id,
                health_score=health_result["health_score"],
                health_breakdown=health_result["health_breakdown"],
                recommendations=health_result["recommendations"],
                strengths=health_result["strengths"],
                weaknesses=health_result["weaknesses"],
                missing_sections=health_result["missing_sections"],
                ats_score=health_result.get("ats_score"),
                formatting_score=health_result.get("formatting_score"),
                readability_score=health_result.get("readability_score"),
            )
        else:
            await repo.create_analysis(
                resume_id=request.resume_id,
                health_score=health_result["health_score"],
                health_breakdown=health_result["health_breakdown"],
                recommendations=health_result["recommendations"],
                strengths=health_result["strengths"],
                weaknesses=health_result["weaknesses"],
                missing_sections=health_result["missing_sections"],
                ats_score=health_result.get("ats_score"),
                formatting_score=health_result.get("formatting_score"),
                readability_score=health_result.get("readability_score"),
            )

        # Create or update metadata record (upsert)
        existing_meta = await repo.get_metadata_by_resume(request.resume_id)
        meta_kwargs = dict(
            resume_id=request.resume_id,
            years_of_experience=parsed_data.get("years_of_experience"),
            primary_domain=parsed_data.get("primary_domain"),
            career_level=parsed_data.get("career_level"),
            total_projects=len(parsed_data.get("projects") or []),
            total_certifications=len(parsed_data.get("certifications") or []),
            total_achievements=len(parsed_data.get("achievements") or []),
            has_leadership_experience=bool(parsed_data.get("has_leadership_experience", False)),
            has_open_source_contributions=bool(parsed_data.get("has_open_source_contributions", False)),
            has_internships=bool(parsed_data.get("has_internships", False)),
            has_research_experience=bool(parsed_data.get("has_research_experience", False)),
            has_publications=bool(parsed_data.get("has_publications", False)),
        )
        if not existing_meta:
            await repo.create_metadata(**meta_kwargs)

        # Delete old parsed records and re-create fresh ones
        await repo.delete_parsed_records(request.resume_id)

        # Create skill records
        skills_data = []
        for category, skills in (parsed_data.get("skills") or {}).items():
            if isinstance(skills, list):
                for skill in skills:
                    if skill:
                        skills_data.append({"name": str(skill), "category": category})
        if skills_data:
            await repo.create_skills(request.resume_id, skills_data)

        # Create experience records
        if parsed_data.get("experience"):
            await repo.create_experience(request.resume_id, parsed_data["experience"])

        # Create education records
        if parsed_data.get("education"):
            await repo.create_education(request.resume_id, parsed_data["education"])

        # Create project records
        if parsed_data.get("projects"):
            await repo.create_projects(request.resume_id, parsed_data["projects"])

        # Create certification records
        if parsed_data.get("certifications"):
            await repo.create_certifications(request.resume_id, parsed_data["certifications"])

        # Create language records
        if parsed_data.get("languages"):
            await repo.create_languages(request.resume_id, parsed_data["languages"])

        # Create achievement records
        if parsed_data.get("achievements"):
            await repo.create_achievements(request.resume_id, parsed_data["achievements"])

        # Create link records
        if parsed_data.get("links"):
            await repo.create_links(request.resume_id, parsed_data["links"])

        logger.info(f"Resume analyzed successfully: {request.resume_id}")

        return ResumeAnalyzeResponse(
            resume_id=request.resume_id,
            analysis=ResumeAnalysisResponse(
                health_score=health_result["health_score"],
                health_breakdown=health_result["health_breakdown"],
                recommendations=health_result["recommendations"],
                strengths=health_result["strengths"],
                weaknesses=health_result["weaknesses"],
                missing_sections=health_result["missing_sections"],
                ats_score=health_result.get("ats_score"),
                formatting_score=health_result.get("formatting_score"),
                readability_score=health_result.get("readability_score"),
            ),
            metadata=ResumeMetadataResponse(
                years_of_experience=parsed_data.get("years_of_experience"),
                primary_domain=parsed_data.get("primary_domain"),
                career_level=parsed_data.get("career_level"),
                total_projects=len(parsed_data.get("projects") or []),
                total_certifications=len(parsed_data.get("certifications") or []),
                total_achievements=len(parsed_data.get("achievements") or []),
                has_leadership_experience=bool(parsed_data.get("has_leadership_experience", False)),
                has_open_source_contributions=bool(parsed_data.get("has_open_source_contributions", False)),
                has_internships=bool(parsed_data.get("has_internships", False)),
                has_research_experience=bool(parsed_data.get("has_research_experience", False)),
                has_publications=bool(parsed_data.get("has_publications", False)),
            ),
        )

    except Exception as e:
        logger.error(f"Failed to analyze resume: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/summary", response_model=ResumeSummaryResponse)
async def generate_resume_summary(
    request: ResumeSummaryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ResumeSummaryResponse:
    """Generate AI-powered resume summary."""
    repo = ResumeRepository(db)
    resume = await repo.get_resume_by_id(request.resume_id)

    if not resume:
        raise NotFoundError("Resume not found")

    if not resume.parsed_data:
        raise ValidationError("Resume must be analyzed before generating summary")

    try:
        # Generate summary
        summary = await summary_service.generate_summary(resume.parsed_data)

        logger.info(f"Resume summary generated: {request.resume_id}")
        return ResumeSummaryResponse(**summary)

    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
