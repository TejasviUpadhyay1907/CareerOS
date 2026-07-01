"""Repository layer for resume data access."""
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    Resume,
    ResumeAchievement,
    ResumeAnalysis,
    ResumeCertification,
    ResumeEducation,
    ResumeExperience,
    ResumeLanguage,
    ResumeLink,
    ResumeMetadata,
    ResumeProject,
    ResumeSkill,
)

logger = get_logger(__name__)


def parse_date(date_str: Any) -> Optional[datetime]:
    """Parse date string to datetime object.
    
    Args:
        date_str: Date string in various formats or datetime object
        
    Returns:
        Parsed datetime object or None
    """
    if not date_str:
        return None
        
    if isinstance(date_str, datetime):
        return date_str
        
    if isinstance(date_str, str):
        # Try common date formats
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d", 
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m",
            "%Y/%m",
            "%m/%Y",
            "%Y",
        ]
        
        for fmt in formats:
            try:
                # For year-only dates, use January 1st
                if fmt == "%Y":
                    return datetime(int(date_str), 1, 1)
                # For year-month dates, use 1st of month
                elif fmt in ["%Y-%m", "%Y/%m", "%m/%Y"]:
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.replace(day=1)
                else:
                    return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        logger.warning(f"Could not parse date: {date_str}")
        return None
    
    return None


class ResumeRepository:
    """Repository for resume data operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    async def create_resume(
        self,
        user_id: str,
        original_filename: str,
        storage_path: str,
        storage_url: str,
        file_size: int,
        mime_type: str,
        raw_text: Optional[str] = None,
        parsed_data: Optional[dict[str, Any]] = None,
    ) -> Resume:
        """Create a new resume record.

        Args:
            user_id: User ID
            original_filename: Original filename
            storage_path: Storage path
            storage_url: Storage URL
            file_size: File size in bytes
            mime_type: MIME type
            raw_text: Extracted raw text
            parsed_data: Parsed resume data

        Returns:
            Created resume record
        """
        resume = Resume(
            user_id=user_id,
            original_filename=original_filename,
            storage_path=storage_path,
            storage_url=storage_url,
            file_size=file_size,
            mime_type=mime_type,
            raw_text=raw_text,
            parsed_data=parsed_data,
        )

        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)

        logger.info(f"Created resume record: {resume.id}")
        return resume

    async def get_resume_by_id(self, resume_id: str) -> Optional[Resume]:
        """Get resume by ID.

        Args:
            resume_id: Resume ID

        Returns:
            Resume record or None
        """
        result = await self.db.execute(
            select(Resume).where(Resume.id == resume_id, Resume.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_resumes_by_user(self, user_id: str) -> list[Resume]:
        """Get all resumes for a user.

        Args:
            user_id: User ID

        Returns:
            List of resume records
        """
        result = await self.db.execute(
            select(Resume)
            .where(Resume.user_id == user_id, Resume.is_deleted == False)
            .order_by(Resume.created_at.desc())
        )
        return result.scalars().all()

    async def update_resume(
        self,
        resume_id: str,
        raw_text: Optional[str] = None,
        parsed_data: Optional[dict[str, Any]] = None,
    ) -> Optional[Resume]:
        """Update resume record.

        Args:
            resume_id: Resume ID
            raw_text: Raw text
            parsed_data: Parsed data

        Returns:
            Updated resume record or None
        """
        resume = await self.get_resume_by_id(resume_id)
        if not resume:
            return None

        if raw_text is not None:
            resume.raw_text = raw_text
        if parsed_data is not None:
            resume.parsed_data = parsed_data

        await self.db.commit()
        await self.db.refresh(resume)

        logger.info(f"Updated resume record: {resume_id}")
        return resume

    async def delete_resume(self, resume_id: str) -> bool:
        """Soft delete a resume.

        Args:
            resume_id: Resume ID

        Returns:
            True if deleted, False otherwise
        """
        resume = await self.get_resume_by_id(resume_id)
        if not resume:
            return False

        resume.is_deleted = True
        await self.db.commit()

        logger.info(f"Deleted resume record: {resume_id}")
        return True

    async def create_analysis(
        self,
        resume_id: str,
        health_score: int,
        health_breakdown: dict[str, int],
        recommendations: list[str],
        strengths: list[str],
        weaknesses: list[str],
        missing_sections: list[str],
        ats_score: Optional[int] = None,
        formatting_score: Optional[int] = None,
        readability_score: Optional[int] = None,
    ) -> ResumeAnalysis:
        """Create resume analysis record.

        Args:
            resume_id: Resume ID
            health_score: Overall health score
            health_breakdown: Health score breakdown
            recommendations: Improvement recommendations
            strengths: Identified strengths
            weaknesses: Identified weaknesses
            missing_sections: Missing sections
            ats_score: ATS score
            formatting_score: Formatting score
            readability_score: Readability score

        Returns:
            Created analysis record
        """
        analysis = ResumeAnalysis(
            resume_id=resume_id,
            health_score=health_score,
            health_breakdown=health_breakdown,
            recommendations=recommendations,
            strengths=strengths,
            weaknesses=weaknesses,
            missing_sections=missing_sections,
            ats_score=ats_score,
            formatting_score=formatting_score,
            readability_score=readability_score,
        )

        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)

        logger.info(f"Created analysis record for resume: {resume_id}")
        return analysis

    async def create_metadata(
        self,
        resume_id: str,
        years_of_experience: Optional[int] = None,
        primary_domain: Optional[str] = None,
        career_level: Optional[str] = None,
        total_projects: int = 0,
        total_certifications: int = 0,
        total_achievements: int = 0,
        has_leadership_experience: bool = False,
        has_open_source_contributions: bool = False,
        has_internships: bool = False,
        has_research_experience: bool = False,
        has_publications: bool = False,
    ) -> ResumeMetadata:
        """Create resume metadata record.

        Args:
            resume_id: Resume ID
            years_of_experience: Years of experience
            primary_domain: Primary domain
            career_level: Career level
            total_projects: Total projects
            total_certifications: Total certifications
            total_achievements: Total achievements
            has_leadership_experience: Has leadership experience
            has_open_source_contributions: Has open source contributions
            has_internships: Has internships
            has_research_experience: Has research experience
            has_publications: Has publications

        Returns:
            Created metadata record
        """
        metadata = ResumeMetadata(
            resume_id=resume_id,
            years_of_experience=years_of_experience,
            primary_domain=primary_domain,
            career_level=career_level,
            total_projects=total_projects,
            total_certifications=total_certifications,
            total_achievements=total_achievements,
            has_leadership_experience=has_leadership_experience,
            has_open_source_contributions=has_open_source_contributions,
            has_internships=has_internships,
            has_research_experience=has_research_experience,
            has_publications=has_publications,
        )

        self.db.add(metadata)
        await self.db.commit()
        await self.db.refresh(metadata)

        logger.info(f"Created metadata record for resume: {resume_id}")
        return metadata

    async def create_skills(self, resume_id: str, skills_data: list[dict[str, Any]]) -> list[ResumeSkill]:
        """Create skill records.

        Args:
            resume_id: Resume ID
            skills_data: List of skill data

        Returns:
            Created skill records
        """
        skills = []
        for skill_data in skills_data:
            skill = ResumeSkill(
                resume_id=resume_id,
                name=skill_data.get("name", ""),
                category=skill_data.get("category", "technical"),
                proficiency=skill_data.get("proficiency"),
                years_experience=skill_data.get("years_experience"),
                is_primary=skill_data.get("is_primary", False),
            )
            self.db.add(skill)
            skills.append(skill)

        await self.db.commit()
        for skill in skills:
            await self.db.refresh(skill)

        logger.info(f"Created {len(skills)} skill records for resume: {resume_id}")
        return skills

    async def create_experience(
        self, resume_id: str, experience_data: list[dict[str, Any]]
    ) -> list[ResumeExperience]:
        """Create experience records.

        Args:
            resume_id: Resume ID
            experience_data: List of experience data

        Returns:
            Created experience records
        """
        experiences = []
        for exp_data in experience_data:
            experience = ResumeExperience(
                resume_id=resume_id,
                company=exp_data.get("company", ""),
                title=exp_data.get("title", ""),
                location=exp_data.get("location"),
                start_date=parse_date(exp_data.get("start_date")),
                end_date=parse_date(exp_data.get("end_date")),
                is_current=exp_data.get("is_current", False),
                description=exp_data.get("description"),
                achievements=exp_data.get("achievements"),
            )
            self.db.add(experience)
            experiences.append(experience)

        await self.db.commit()
        for exp in experiences:
            await self.db.refresh(exp)

        logger.info(f"Created {len(experiences)} experience records for resume: {resume_id}")
        return experiences

    async def create_education(
        self, resume_id: str, education_data: list[dict[str, Any]]
    ) -> list[ResumeEducation]:
        """Create education records.

        Args:
            resume_id: Resume ID
            education_data: List of education data

        Returns:
            Created education records
        """
        educations = []
        for edu_data in education_data:
            # Handle GPA as string or float
            gpa_raw = edu_data.get("gpa")
            gpa = None
            if gpa_raw is not None:
                try:
                    # Handle formats like "8.5/10", "3.8", "3.8/4.0"
                    gpa_str = str(gpa_raw).strip()
                    if "/" in gpa_str:
                        gpa = float(gpa_str.split("/")[0])
                    else:
                        gpa = float(gpa_str)
                except (ValueError, TypeError):
                    gpa = None
            education = ResumeEducation(
                resume_id=resume_id,
                institution=edu_data.get("institution", ""),
                degree=edu_data.get("degree", ""),
                field_of_study=edu_data.get("field_of_study"),
                location=edu_data.get("location"),
                start_date=parse_date(edu_data.get("start_date")),
                end_date=parse_date(edu_data.get("end_date")),
                gpa=gpa,
                honors=edu_data.get("honors"),
            )
            self.db.add(education)
            educations.append(education)

        await self.db.commit()
        for edu in educations:
            await self.db.refresh(edu)

        logger.info(f"Created {len(educations)} education records for resume: {resume_id}")
        return educations

    async def create_projects(
        self, resume_id: str, projects_data: list[dict[str, Any]]
    ) -> list[ResumeProject]:
        """Create project records.

        Args:
            resume_id: Resume ID
            projects_data: List of project data

        Returns:
            Created project records
        """
        projects = []
        for proj_data in projects_data:
            project = ResumeProject(
                resume_id=resume_id,
                name=proj_data.get("name", ""),
                description=proj_data.get("description"),
                url=proj_data.get("url"),
                start_date=parse_date(proj_data.get("start_date")),
                end_date=parse_date(proj_data.get("end_date")),
                technologies=proj_data.get("technologies", []),
                achievements=proj_data.get("achievements"),
            )
            self.db.add(project)
            projects.append(project)

        await self.db.commit()
        for proj in projects:
            await self.db.refresh(proj)

        logger.info(f"Created {len(projects)} project records for resume: {resume_id}")
        return projects

    async def create_certifications(
        self, resume_id: str, certs_data: list[dict[str, Any]]
    ) -> list[ResumeCertification]:
        """Create certification records."""
        certs = []
        for cert_data in certs_data:
            cert = ResumeCertification(
                resume_id=resume_id,
                name=cert_data.get("name", ""),
                issuer=cert_data.get("issuer", ""),
                issue_date=parse_date(cert_data.get("issue_date")),
                expiration_date=parse_date(cert_data.get("expiration_date")),
                credential_id=cert_data.get("credential_id"),
                url=cert_data.get("url"),
            )
            self.db.add(cert)
            certs.append(cert)

        await self.db.commit()
        for cert in certs:
            await self.db.refresh(cert)

        logger.info(f"Created {len(certs)} certification records for resume: {resume_id}")
        return certs

    async def create_languages(
        self, resume_id: str, languages_data: list[dict[str, Any]]
    ) -> list[ResumeLanguage]:
        """Create language records."""
        langs = []
        for lang_data in languages_data:
            lang = ResumeLanguage(
                resume_id=resume_id,
                name=lang_data.get("name", ""),
                proficiency=lang_data.get("proficiency", "intermediate"),
            )
            self.db.add(lang)
            langs.append(lang)

        await self.db.commit()
        for lang in langs:
            await self.db.refresh(lang)

        logger.info(f"Created {len(langs)} language records for resume: {resume_id}")
        return langs

    async def create_achievements(
        self, resume_id: str, achievements_data: list[dict[str, Any]]
    ) -> list[ResumeAchievement]:
        """Create achievement records."""
        achievements = []
        for ach_data in achievements_data:
            ach = ResumeAchievement(
                resume_id=resume_id,
                title=ach_data.get("title", ""),
                description=ach_data.get("description"),
                date=parse_date(ach_data.get("date")),
                category=ach_data.get("category"),
            )
            self.db.add(ach)
            achievements.append(ach)

        await self.db.commit()
        for ach in achievements:
            await self.db.refresh(ach)

        logger.info(f"Created {len(achievements)} achievement records for resume: {resume_id}")
        return achievements

    async def create_links(
        self, resume_id: str, links_data: list[dict[str, Any]]
    ) -> list[ResumeLink]:
        """Create link records."""
        links = []
        for link_data in links_data:
            link = ResumeLink(
                resume_id=resume_id,
                type=link_data.get("type", "other"),
                url=link_data.get("url", ""),
                label=link_data.get("label"),
            )
            self.db.add(link)
            links.append(link)

        await self.db.commit()
        for link in links:
            await self.db.refresh(link)

        logger.info(f"Created {len(links)} link records for resume: {resume_id}")
        return links

    async def get_analysis_by_resume(self, resume_id: str) -> Optional[ResumeAnalysis]:
        """Get analysis for a resume."""
        from app.db.models.resume import ResumeAnalysis as _RA
        result = await self.db.execute(
            select(_RA).where(_RA.resume_id == resume_id)
        )
        return result.scalar_one_or_none()

    async def update_analysis(
        self,
        resume_id: str,
        health_score: int,
        health_breakdown: dict,
        recommendations: list,
        strengths: list,
        weaknesses: list,
        missing_sections: list,
        ats_score: Optional[int] = None,
        formatting_score: Optional[int] = None,
        readability_score: Optional[int] = None,
    ) -> Optional[ResumeAnalysis]:
        """Update existing analysis record."""
        analysis = await self.get_analysis_by_resume(resume_id)
        if not analysis:
            return None
        analysis.health_score = health_score
        analysis.health_breakdown = health_breakdown
        analysis.recommendations = recommendations
        analysis.strengths = strengths
        analysis.weaknesses = weaknesses
        analysis.missing_sections = missing_sections
        analysis.ats_score = ats_score
        analysis.formatting_score = formatting_score
        analysis.readability_score = readability_score
        await self.db.commit()
        await self.db.refresh(analysis)
        return analysis

    async def get_metadata_by_resume(self, resume_id: str) -> Optional[ResumeMetadata]:
        """Get metadata for a resume."""
        result = await self.db.execute(
            select(ResumeMetadata).where(ResumeMetadata.resume_id == resume_id)
        )
        return result.scalar_one_or_none()

    async def delete_parsed_records(self, resume_id: str) -> None:
        """Delete all parsed sub-records for a resume so re-analysis is clean."""
        from sqlalchemy import delete
        for model in (ResumeSkill, ResumeExperience, ResumeEducation,
                      ResumeProject, ResumeCertification, ResumeLanguage,
                      ResumeAchievement, ResumeLink):
            await self.db.execute(
                delete(model).where(model.resume_id == resume_id)
            )
        await self.db.commit()
        logger.info(f"Deleted parsed records for resume: {resume_id}")
