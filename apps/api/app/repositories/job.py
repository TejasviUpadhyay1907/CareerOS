"""Repository layer for job data access."""
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    ATSAnalysis,
    Job,
    JobAnalysis,
    JobBenefit,
    JobKeyword,
    JobRequirement,
    JobResponsibility,
    JobSkill,
    MatchRecommendation,
    MissingSkill,
    ResumeJobMatch,
)

logger = get_logger(__name__)


class JobRepository:
    """Repository for job data operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    async def create_job(
        self,
        user_id: str,
        title: str,
        company_name: str,
        raw_description: str,
        parsed_data: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> Job:
        """Create a new job record.

        Args:
            user_id: User ID
            title: Job title
            company_name: Company name
            raw_description: Raw job description
            parsed_data: Parsed job data
            **kwargs: Additional job fields

        Returns:
            Created job record
        """
        job = Job(
            user_id=user_id,
            title=title,
            company_name=company_name,
            raw_description=raw_description,
            parsed_data=parsed_data,
            **kwargs,
        )

        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)

        logger.info(f"Created job record: {job.id}")
        return job

    async def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Get job by ID.

        Args:
            job_id: Job ID

        Returns:
            Job record or None
        """
        result = await self.db.execute(
            select(Job).where(Job.id == job_id, Job.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_jobs_by_user(self, user_id: str) -> list[Job]:
        """Get all jobs for a user.

        Args:
            user_id: User ID

        Returns:
            List of job records
        """
        result = await self.db.execute(
            select(Job)
            .where(Job.user_id == user_id, Job.is_deleted == False)
            .order_by(Job.created_at.desc())
        )
        return result.scalars().all()

    async def delete_job(self, job_id: str) -> bool:
        """Soft delete a job.

        Args:
            job_id: Job ID

        Returns:
            True if deleted, False otherwise
        """
        job = await self.get_job_by_id(job_id)
        if not job:
            return False

        job.is_deleted = True
        await self.db.commit()

        logger.info(f"Deleted job record: {job_id}")
        return True

    async def create_job_skills(self, job_id: str, skills_data: list[dict[str, Any]]) -> list[JobSkill]:
        """Create job skill records.

        Args:
            job_id: Job ID
            skills_data: List of skill data

        Returns:
            Created skill records
        """
        skills = []
        for skill_data in skills_data:
            skill = JobSkill(
                job_id=job_id,
                name=skill_data.get("name", ""),
                category=skill_data.get("category", "required"),
                type=skill_data.get("type", "technical"),
                importance=skill_data.get("importance"),
            )
            self.db.add(skill)
            skills.append(skill)

        await self.db.commit()
        for skill in skills:
            await self.db.refresh(skill)

        logger.info(f"Created {len(skills)} job skill records for job: {job_id}")
        return skills

    async def create_job_requirements(
        self, job_id: str, requirements_data: list[dict[str, Any]]
    ) -> list[JobRequirement]:
        """Create job requirement records.

        Args:
            job_id: Job ID
            requirements_data: List of requirement data

        Returns:
            Created requirement records
        """
        requirements = []
        for req_data in requirements_data:
            requirement = JobRequirement(
                job_id=job_id,
                requirement=req_data.get("requirement", ""),
                category=req_data.get("category"),
                is_mandatory=req_data.get("is_mandatory", False),
            )
            self.db.add(requirement)
            requirements.append(requirement)

        await self.db.commit()
        for req in requirements:
            await self.db.refresh(req)

        logger.info(f"Created {len(requirements)} job requirement records for job: {job_id}")
        return requirements

    async def create_job_responsibilities(
        self, job_id: str, responsibilities_data: list[dict[str, Any]]
    ) -> list[JobResponsibility]:
        """Create job responsibility records.

        Args:
            job_id: Job ID
            responsibilities_data: List of responsibility data

        Returns:
            Created responsibility records
        """
        responsibilities = []
        for resp_data in responsibilities_data:
            responsibility = JobResponsibility(
                job_id=job_id,
                responsibility=resp_data.get("responsibility", ""),
                priority=resp_data.get("priority"),
            )
            self.db.add(responsibility)
            responsibilities.append(responsibility)

        await self.db.commit()
        for resp in responsibilities:
            await self.db.refresh(resp)

        logger.info(f"Created {len(responsibilities)} job responsibility records for job: {job_id}")
        return responsibilities

    async def create_job_benefits(
        self, job_id: str, benefits_data: list[dict[str, Any]]
    ) -> list[JobBenefit]:
        """Create job benefit records.

        Args:
            job_id: Job ID
            benefits_data: List of benefit data

        Returns:
            Created benefit records
        """
        benefits = []
        for benefit_data in benefits_data:
            benefit = JobBenefit(
                job_id=job_id,
                benefit=benefit_data.get("benefit", ""),
                category=benefit_data.get("category"),
            )
            self.db.add(benefit)
            benefits.append(benefit)

        await self.db.commit()
        for benefit in benefits:
            await self.db.refresh(benefit)

        logger.info(f"Created {len(benefits)} job benefit records for job: {job_id}")
        return benefits

    async def create_job_analysis(
        self,
        job_id: str,
        hiring_signals: list[str],
        urgency: str,
        leadership_required: bool,
        communication_level: str,
        growth_potential: str,
        work_life_balance: str,
        company_culture_indicators: list[str],
        hidden_expectations: list[str],
        **kwargs,
    ) -> JobAnalysis:
        """Create job analysis record.

        Args:
            job_id: Job ID
            hiring_signals: Hiring signals
            urgency: Urgency level
            leadership_required: Leadership required
            communication_level: Communication level
            growth_potential: Growth potential
            work_life_balance: Work life balance
            company_culture_indicators: Company culture indicators
            hidden_expectations: Hidden expectations
            **kwargs: Additional analysis fields

        Returns:
            Created analysis record
        """
        analysis = JobAnalysis(
            job_id=job_id,
            hiring_signals=hiring_signals,
            urgency=urgency,
            leadership_required=leadership_required,
            communication_level=communication_level,
            growth_potential=growth_potential,
            work_life_balance=work_life_balance,
            company_culture_indicators=company_culture_indicators,
            hidden_expectations=hidden_expectations,
            **kwargs,
        )

        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)

        logger.info(f"Created job analysis record for job: {job_id}")
        return analysis

    async def create_resume_job_match(
        self,
        job_id: str,
        resume_id: str,
        match_data: dict[str, Any],
    ) -> ResumeJobMatch:
        """Create resume-job match record.

        Args:
            job_id: Job ID
            resume_id: Resume ID
            match_data: Match analysis data

        Returns:
            Created match record
        """
        match = ResumeJobMatch(
            job_id=job_id,
            resume_id=resume_id,
            overall_match=match_data.get("overall_match", 0),
            technical_match=match_data.get("technical_match", 0),
            experience_match=match_data.get("experience_match", 0),
            education_match=match_data.get("education_match", 0),
            project_match=match_data.get("project_match", 0),
            keyword_match=match_data.get("keyword_match", 0),
            ats_match=match_data.get("ats_match", 0),
            leadership_match=match_data.get("leadership_match", 0),
            communication_match=match_data.get("communication_match", 0),
            industry_match=match_data.get("industry_match", 0),
            confidence_score=match_data.get("confidence_score", 0),
            match_reasoning=match_data.get("match_reasoning", {}),
        )

        self.db.add(match)
        await self.db.commit()
        await self.db.refresh(match)

        logger.info(f"Created resume-job match record: {match.id}")
        return match

    async def create_ats_analysis(
        self,
        match_id: str,
        ats_data: dict[str, Any],
    ) -> ATSAnalysis:
        """Create ATS analysis record.

        Args:
            match_id: Match ID
            ats_data: ATS analysis data

        Returns:
            Created ATS analysis record
        """
        analysis = ATSAnalysis(
            match_id=match_id,
            keyword_coverage=ats_data.get("keyword_coverage", 0),
            formatting_compatibility=ats_data.get("formatting_compatibility", 0),
            action_verbs_score=ats_data.get("action_verbs_score", 0),
            role_alignment=ats_data.get("role_alignment", 0),
            missing_keywords=ats_data.get("missing_keywords", []),
            resume_length_score=ats_data.get("resume_length_score", 0),
            section_completeness=ats_data.get("section_completeness", 0),
            optimization_potential=ats_data.get("optimization_potential", 0),
            detailed_report=ats_data.get("detailed_report", {}),
        )

        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)

        logger.info(f"Created ATS analysis record for match: {match_id}")
        return analysis

    async def create_missing_skills(
        self,
        match_id: str,
        missing_skills_data: list[dict[str, Any]],
    ) -> list[MissingSkill]:
        """Create missing skill records.

        Args:
            match_id: Match ID
            missing_skills_data: List of missing skill data

        Returns:
            Created missing skill records
        """
        skills = []
        for skill_data in missing_skills_data:
            skill = MissingSkill(
                match_id=match_id,
                skill_name=skill_data.get("skill_name", ""),
                category=skill_data.get("category", ""),
                learning_priority=skill_data.get("learning_priority", ""),
                estimated_learning_time=skill_data.get("estimated_learning_time"),
                difficulty=skill_data.get("difficulty"),
                free_resources=skill_data.get("free_resources", []),
            )
            self.db.add(skill)
            skills.append(skill)

        await self.db.commit()
        for skill in skills:
            await self.db.refresh(skill)

        logger.info(f"Created {len(skills)} missing skill records for match: {match_id}")
        return skills
