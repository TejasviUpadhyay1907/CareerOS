"""Repository layer for application accelerator data access."""
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    CoverLetter,
    GeneratedDocument,
    InterviewKit,
    OptimizedResume,
    RecruiterMessage,
)

logger = get_logger(__name__)


class AcceleratorRepository:
    """Repository for application accelerator operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    async def create_optimized_resume(
        self,
        user_id: str,
        resume_id: str,
        job_id: str,
        original_content: str,
        optimized_content: str,
        changes: dict[str, Any],
        optimization_score: int,
        estimated_ats_improvement: int,
        estimated_match_increase: int,
        estimated_interview_probability: int,
    ) -> OptimizedResume:
        """Create optimized resume record.

        Args:
            user_id: User ID
            resume_id: Resume ID
            job_id: Job ID
            original_content: Original resume content
            optimized_content: Optimized resume content
            changes: Changes made
            optimization_score: Optimization score
            estimated_ats_improvement: Estimated ATS improvement
            estimated_match_increase: Estimated match increase
            estimated_interview_probability: Estimated interview probability

        Returns:
            Created optimized resume
        """
        optimized_resume = OptimizedResume(
            user_id=user_id,
            resume_id=resume_id,
            job_id=job_id,
            original_resume_content=original_content,
            optimized_content=optimized_content,
            changes=changes,
            optimization_score=optimization_score,
            estimated_ats_improvement=estimated_ats_improvement,
            estimated_match_increase=estimated_match_increase,
            estimated_interview_probability=estimated_interview_probability,
            version_number=1,
        )

        self.db.add(optimized_resume)
        await self.db.commit()
        await self.db.refresh(optimized_resume)

        logger.info(f"Created optimized resume: {optimized_resume.id}")
        return optimized_resume

    async def create_cover_letter(
        self,
        user_id: str,
        resume_id: str,
        job_id: str,
        content: str,
        tone: str,
        length: str,
        company_name: str,
        role_title: str,
        personalization_points: list[dict[str, Any]],
    ) -> CoverLetter:
        """Create cover letter record.

        Args:
            user_id: User ID
            resume_id: Resume ID
            job_id: Job ID
            content: Cover letter content
            tone: Tone
            length: Length
            company_name: Company name
            role_title: Role title
            personalization_points: Personalization points

        Returns:
            Created cover letter
        """
        cover_letter = CoverLetter(
            user_id=user_id,
            resume_id=resume_id,
            job_id=job_id,
            content=content,
            tone=tone,
            length=length,
            company_name=company_name,
            role_title=role_title,
            personalization_points=personalization_points,
            version_number=1,
        )

        self.db.add(cover_letter)
        await self.db.commit()
        await self.db.refresh(cover_letter)

        logger.info(f"Created cover letter: {cover_letter.id}")
        return cover_letter

    async def create_recruiter_message(
        self,
        user_id: str,
        resume_id: str,
        job_id: Optional[str],
        message_type: str,
        subject: Optional[str],
        content: str,
        tone: str,
        length: str,
        personalization_reason: str,
        call_to_action: str,
        recipient_name: Optional[str],
        recipient_company: Optional[str],
        platform: str,
    ) -> RecruiterMessage:
        """Create recruiter message record.

        Args:
            user_id: User ID
            resume_id: Resume ID
            job_id: Job ID
            message_type: Message type
            subject: Subject
            content: Message content
            tone: Tone
            length: Length
            personalization_reason: Personalization reason
            call_to_action: Call to action
            recipient_name: Recipient name
            recipient_company: Recipient company
            platform: Platform

        Returns:
            Created recruiter message
        """
        message = RecruiterMessage(
            user_id=user_id,
            resume_id=resume_id,
            job_id=job_id,
            message_type=message_type,
            subject=subject,
            content=content,
            tone=tone,
            length=length,
            personalization_reason=personalization_reason,
            call_to_action=call_to_action,
            recipient_name=recipient_name,
            recipient_company=recipient_company,
            platform=platform,
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        logger.info(f"Created recruiter message: {message.id}")
        return message

    async def create_interview_kit(
        self,
        user_id: str,
        resume_id: str,
        job_id: str,
        company_overview: str,
        role_overview: str,
        responsibilities: list[str],
        technical_topics: list[dict[str, Any]],
        behavioral_questions: list[dict[str, Any]],
        star_suggestions: list[dict[str, Any]],
        project_questions: list[dict[str, Any]],
        resume_questions: list[dict[str, Any]],
        coding_topics: list[dict[str, Any]],
        system_design_topics: list[dict[str, Any]],
        hr_questions: list[dict[str, Any]],
        salary_tips: list[str],
        questions_to_ask: list[dict[str, Any]],
        study_plan_90min: list[dict[str, Any]],
        study_plan_3day: list[dict[str, Any]],
        study_plan_7day: list[dict[str, Any]],
        priority_ranking: dict[str, Any],
    ) -> InterviewKit:
        """Create interview kit record.

        Args:
            user_id: User ID
            resume_id: Resume ID
            job_id: Job ID
            company_overview: Company overview
            role_overview: Role overview
            responsibilities: Responsibilities
            technical_topics: Technical topics
            behavioral_questions: Behavioral questions
            star_suggestions: STAR suggestions
            project_questions: Project questions
            resume_questions: Resume questions
            coding_topics: Coding topics
            system_design_topics: System design topics
            hr_questions: HR questions
            salary_tips: Salary tips
            questions_to_ask: Questions to ask
            study_plan_90min: 90-minute study plan
            study_plan_3day: 3-day study plan
            study_plan_7day: 7-day study plan
            priority_ranking: Priority ranking

        Returns:
            Created interview kit
        """
        kit = InterviewKit(
            user_id=user_id,
            resume_id=resume_id,
            job_id=job_id,
            company_overview=company_overview,
            role_overview=role_overview,
            responsibilities=responsibilities,
            technical_topics=technical_topics,
            behavioral_questions=behavioral_questions,
            star_suggestions=star_suggestions,
            project_questions=project_questions,
            resume_questions=resume_questions,
            coding_topics=coding_topics,
            system_design_topics=system_design_topics,
            hr_questions=hr_questions,
            salary_tips=salary_tips,
            questions_to_ask=questions_to_ask,
            study_plan_90min=study_plan_90min,
            study_plan_3day=study_plan_3day,
            study_plan_7day=study_plan_7day,
            priority_ranking=priority_ranking,
        )

        self.db.add(kit)
        await self.db.commit()
        await self.db.refresh(kit)

        logger.info(f"Created interview kit: {kit.id}")
        return kit

    async def create_generated_document(
        self,
        user_id: str,
        document_type: str,
        document_id: str,
        title: str,
        description: Optional[str],
        format: str,
        file_path: Optional[str],
        file_size: Optional[int],
    ) -> GeneratedDocument:
        """Create generated document record.

        Args:
            user_id: User ID
            document_type: Document type
            document_id: Document ID
            title: Title
            description: Description
            format: Format
            file_path: File path
            file_size: File size

        Returns:
            Created generated document
        """
        document = GeneratedDocument(
            user_id=user_id,
            document_type=document_type,
            document_id=document_id,
            title=title,
            description=description,
            format=format,
            file_path=file_path,
            file_size=file_size,
            export_count=0,
        )

        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)

        logger.info(f"Created generated document: {document.id}")
        return document

    async def get_optimized_resumes(
        self, user_id: str, resume_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[OptimizedResume]:
        """Get optimized resumes for user.

        Args:
            user_id: User ID
            resume_id: Filter by resume ID
            job_id: Filter by job ID

        Returns:
            List of optimized resumes
        """
        query = select(OptimizedResume).where(
            OptimizedResume.user_id == user_id, OptimizedResume.is_deleted == False
        )

        if resume_id:
            query = query.where(OptimizedResume.resume_id == resume_id)
        if job_id:
            query = query.where(OptimizedResume.job_id == job_id)

        query = query.order_by(OptimizedResume.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_cover_letters(
        self, user_id: str, resume_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[CoverLetter]:
        """Get cover letters for user.

        Args:
            user_id: User ID
            resume_id: Filter by resume ID
            job_id: Filter by job ID

        Returns:
            List of cover letters
        """
        query = select(CoverLetter).where(
            CoverLetter.user_id == user_id, CoverLetter.is_deleted == False
        )

        if resume_id:
            query = query.where(CoverLetter.resume_id == resume_id)
        if job_id:
            query = query.where(CoverLetter.job_id == job_id)

        query = query.order_by(CoverLetter.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_interview_kits(
        self, user_id: str, resume_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[InterviewKit]:
        """Get interview kits for user.

        Args:
            user_id: User ID
            resume_id: Filter by resume ID
            job_id: Filter by job ID

        Returns:
            List of interview kits
        """
        query = select(InterviewKit).where(
            InterviewKit.user_id == user_id, InterviewKit.is_deleted == False
        )

        if resume_id:
            query = query.where(InterviewKit.resume_id == resume_id)
        if job_id:
            query = query.where(InterviewKit.job_id == job_id)

        query = query.order_by(InterviewKit.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_recruiter_messages(
        self, user_id: str, resume_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[RecruiterMessage]:
        """Get recruiter messages for user.

        Args:
            user_id: User ID
            resume_id: Filter by resume ID
            job_id: Filter by job ID

        Returns:
            List of recruiter messages
        """
        query = select(RecruiterMessage).where(
            RecruiterMessage.user_id == user_id, RecruiterMessage.is_deleted == False
        )

        if resume_id:
            query = query.where(RecruiterMessage.resume_id == resume_id)
        if job_id:
            query = query.where(RecruiterMessage.job_id == job_id)

        query = query.order_by(RecruiterMessage.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_generated_documents(self, user_id: str) -> list[GeneratedDocument]:
        """Get generated documents for user.

        Args:
            user_id: User ID

        Returns:
            List of generated documents
        """
        query = select(GeneratedDocument).where(
            GeneratedDocument.user_id == user_id, GeneratedDocument.is_deleted == False
        ).order_by(GeneratedDocument.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()
