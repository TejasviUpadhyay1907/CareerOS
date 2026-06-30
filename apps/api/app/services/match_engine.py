"""Match engine for resume-job comparison."""
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class MatchEngine:
    """Service for calculating resume-job match scores."""

    def calculate_match(
        self, resume_data: dict[str, Any], job_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Calculate comprehensive match scores between resume and job.

        Args:
            resume_data: Parsed resume data
            job_data: Parsed job data

        Returns:
            Match scores and reasoning
        """
        reasoning = {}

        # Technical match
        technical_match, technical_reasoning = self._calculate_technical_match(resume_data, job_data)
        reasoning["technical"] = technical_reasoning

        # Experience match
        experience_match, experience_reasoning = self._calculate_experience_match(resume_data, job_data)
        reasoning["experience"] = experience_reasoning

        # Education match
        education_match, education_reasoning = self._calculate_education_match(resume_data, job_data)
        reasoning["education"] = education_reasoning

        # Project match
        project_match, project_reasoning = self._calculate_project_match(resume_data, job_data)
        reasoning["project"] = project_reasoning

        # Keyword match
        keyword_match, keyword_reasoning = self._calculate_keyword_match(resume_data, job_data)
        reasoning["keyword"] = keyword_reasoning

        # Leadership match
        leadership_match, leadership_reasoning = self._calculate_leadership_match(resume_data, job_data)
        reasoning["leadership"] = leadership_reasoning

        # Communication match
        communication_match, communication_reasoning = self._calculate_communication_match(resume_data, job_data)
        reasoning["communication"] = communication_reasoning

        # Industry match
        industry_match, industry_reasoning = self._calculate_industry_match(resume_data, job_data)
        reasoning["industry"] = industry_reasoning

        # Calculate overall match (weighted average)
        weights = {
            "technical": 0.25,
            "experience": 0.20,
            "education": 0.10,
            "project": 0.15,
            "keyword": 0.10,
            "leadership": 0.05,
            "communication": 0.05,
            "industry": 0.10,
        }

        overall_match = int(
            sum(
                weights[key]
                * {
                    "technical": technical_match,
                    "experience": experience_match,
                    "education": education_match,
                    "project": project_match,
                    "keyword": keyword_match,
                    "leadership": leadership_match,
                    "communication": communication_match,
                    "industry": industry_match,
                }[key]
                for key in weights
            )
        )

        # Calculate confidence score based on data completeness
        confidence_score = self._calculate_confidence_score(resume_data, job_data)

        # ATS match (simplified for now, will be enhanced by ATS service)
        ats_match = int((technical_match * 0.4 + keyword_match * 0.3 + experience_match * 0.3))
        reasoning["ats"] = f"Based on technical ({technical_match}), keyword ({keyword_match}), and experience ({experience_match}) matches"

        return {
            "overall_match": overall_match,
            "technical_match": technical_match,
            "experience_match": experience_match,
            "education_match": education_match,
            "project_match": project_match,
            "keyword_match": keyword_match,
            "ats_match": ats_match,
            "leadership_match": leadership_match,
            "communication_match": communication_match,
            "industry_match": industry_match,
            "confidence_score": confidence_score,
            "match_reasoning": reasoning,
        }

    def _calculate_technical_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate technical skills match."""
        resume_skills = set()
        if resume.get("skills"):
            resume_skills.update(resume["skills"].get("technical", []))
            resume_skills.update(resume["skills"].get("tools", []))

        job_required = set(job.get("required_skills", []))
        job_preferred = set(job.get("preferred_skills", []))
        job_tools = set(job.get("tools", []))
        job_frameworks = set(job.get("frameworks", []))
        job_languages = set(job.get("programming_languages", []))

        all_job_skills = job_required | job_preferred | job_tools | job_frameworks | job_languages

        if not all_job_skills:
            return 100, "No technical skills specified in job"

        matched = resume_skills & all_job_skills
        required_matched = resume_skills & job_required

        # Weight required skills more heavily — guard against zero division
        if job_required:
            required_score = (len(required_matched) / len(job_required)) * 70
            optional_skills = all_job_skills - job_required
            if optional_skills:
                additional_score = (len(matched - required_matched) / len(optional_skills)) * 30
            else:
                additional_score = 30 if required_matched else 0
            match_score = int(required_score + additional_score)
        else:
            match_score = int((len(matched) / len(all_job_skills)) * 100) if all_job_skills else 50

        reasoning = f"Matched {len(matched)}/{len(all_job_skills)} technical skills ({len(required_matched)}/{len(job_required)} required)"
        return match_score, reasoning

    def _calculate_experience_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate experience match."""
        resume_years = resume.get("years_of_experience", 0)
        job_exp_required = job.get("experience_required", "")

        # Parse job experience requirement
        job_min_years = 0
        if job_exp_required and "year" in job_exp_required.lower():
            import re
            numbers = re.findall(r"\d+", job_exp_required)
            if numbers:
                job_min_years = int(numbers[0])

        if job_min_years == 0:
            return 100, "No specific experience requirement"

        if resume_years >= job_min_years:
            # Bonus for exceeding requirement
            excess = resume_years - job_min_years
            bonus = min(excess * 2, 10)  # Max 10 bonus points
            match_score = min(100 + bonus, 100)
            reasoning = f"Has {resume_years} years vs {job_min_years} required (exceeds by {excess} years)"
        else:
            deficit = job_min_years - resume_years
            match_score = max(100 - (deficit * 15), 0)
            reasoning = f"Has {resume_years} years vs {job_min_years} required (short by {deficit} years)"

        return int(match_score), reasoning

    def _calculate_education_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate education match."""
        job_education = (job.get("education_required") or "").lower()

        if not job_education or "any" in job_education:
            return 100, "No specific education requirement"

        resume_education = resume.get("education", [])
        if not resume_education:
            return 0, "No education found in resume"

        # Check for degree match
        has_bachelor = any("bachelor" in edu.get("degree", "").lower() for edu in resume_education)
        has_master = any("master" in edu.get("degree", "").lower() for edu in resume_education)
        has_phd = any("phd" in edu.get("degree", "").lower() or "doctor" in edu.get("degree", "").lower() for edu in resume_education)

        if "bachelor" in job_education:
            if has_bachelor or has_master or has_phd:
                match_score = 100
                reasoning = "Meets bachelor's requirement"
            else:
                match_score = 0
                reasoning = "Missing bachelor's degree"
        elif "master" in job_education:
            if has_master or has_phd:
                match_score = 100
                reasoning = "Meets master's requirement"
            elif has_bachelor:
                match_score = 60
                reasoning = "Has bachelor's but master's preferred"
            else:
                match_score = 0
                reasoning = "Missing required education"
        elif "phd" in job_education or "doctor" in job_education:
            if has_phd:
                match_score = 100
                reasoning = "Meets PhD requirement"
            elif has_master:
                match_score = 70
                reasoning = "Has master's but PhD preferred"
            else:
                match_score = 30
                reasoning = "Education below PhD requirement"
        else:
            match_score = 100
            reasoning = "Education requirement met"

        return match_score, reasoning

    def _calculate_project_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate project match."""
        resume_projects = resume.get("projects", [])
        job_tools = set(job.get("tools", []))
        job_frameworks = set(job.get("frameworks", []))
        job_languages = set(job.get("programming_languages", []))
        job_tech = job_tools | job_frameworks | job_languages

        if not resume_projects:
            return 0, "No projects in resume"

        if not job_tech:
            return 100, "No specific technology requirements"

        # Count projects using job technologies
        matching_projects = 0
        for project in resume_projects:
            project_tech = set(project.get("technologies", []))
            if project_tech & job_tech:
                matching_projects += 1

        match_score = int((matching_projects / len(resume_projects)) * 100)
        reasoning = f"{matching_projects}/{len(resume_projects)} projects use required technologies"
        return match_score, reasoning

    def _calculate_keyword_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate keyword match."""
        job_keywords = set(job.get("keywords", []))

        if not job_keywords:
            return 100, "No keywords specified"

        # Extract keywords from resume
        resume_text = " ".join(
            resume.get("skills", {}).get("technical", [])
            + resume.get("skills", {}).get("soft", [])
            + [exp.get("title", "") for exp in resume.get("experience", [])]
        ).lower()

        matched_keywords = sum(1 for keyword in job_keywords if keyword.lower() in resume_text)
        match_score = int((matched_keywords / len(job_keywords)) * 100)
        reasoning = f"Matched {matched_keywords}/{len(job_keywords)} keywords"
        return match_score, reasoning

    def _calculate_leadership_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate leadership match."""
        job_requires_leadership = job.get("leadership_required", False)
        resume_has_leadership = resume.get("has_leadership_experience", False)

        if not job_requires_leadership:
            return 100, "Leadership not required"

        if resume_has_leadership:
            return 100, "Has leadership experience"
        else:
            return 0, "Missing leadership experience"

    def _calculate_communication_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate communication match."""
        job_level = job.get("communication_level", "intermediate")

        # Check for soft skills in resume
        resume_soft_skills = resume.get("skills", {}).get("soft", [])
        communication_keywords = ["communication", "collaboration", "teamwork", "presentation", "public speaking"]

        has_communication = any(
            any(keyword in skill.lower() for keyword in communication_keywords)
            for skill in resume_soft_skills
        )

        if job_level == "basic":
            return 100, "Basic communication requirement met"
        elif job_level == "intermediate":
            return 100 if has_communication else 60, "Communication skills present" if has_communication else "Limited communication evidence"
        elif job_level == "advanced":
            return 100 if has_communication else 40, "Strong communication evidence" if has_communication else "Communication skills may be lacking"
        else:  # expert
            return 100 if has_communication else 20, "Expert communication" if has_communication else "Communication skills insufficient"

    def _calculate_industry_match(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, str]:
        """Calculate industry match."""
        job_industry = (job.get("industry") or "").lower()
        resume_domain = (resume.get("primary_domain") or "").lower()

        if not job_industry:
            return 100, "No industry specified"

        if not resume_domain:
            return 50, "No domain specified in resume"

        if job_industry in resume_domain or resume_domain in job_industry:
            return 100, f"Industry match: {job_industry}"
        else:
            return 30, f"Industry mismatch: resume in {resume_domain}, job in {job_industry}"

    def _calculate_confidence_score(self, resume: dict[str, Any], job: dict[str, Any]) -> int:
        """Calculate confidence score based on data completeness."""
        score = 100

        # Penalize missing resume data
        if not resume.get("experience"):
            score -= 20
        if not resume.get("skills") or not any(resume["skills"].values()):
            score -= 15
        if not resume.get("education"):
            score -= 10
        if not resume.get("projects"):
            score -= 10

        # Penalize missing job data
        if not job.get("required_skills"):
            score -= 10
        if not job.get("responsibilities"):
            score -= 5

        return max(score, 0)


# Global instance
match_engine = MatchEngine()
