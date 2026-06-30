"""ATS analysis service."""
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class ATSService:
    """Service for ATS (Applicant Tracking System) analysis."""

    def analyze_ats(self, resume_data: dict[str, Any], job_data: dict[str, Any]) -> dict[str, Any]:
        """Perform comprehensive ATS analysis.

        Args:
            resume_data: Parsed resume data
            job_data: Parsed job data

        Returns:
            ATS analysis results
        """
        # Keyword coverage
        keyword_coverage, missing_keywords = self._analyze_keyword_coverage(resume_data, job_data)

        # Formatting compatibility
        formatting_compatibility = self._analyze_formatting(resume_data)

        # Action verbs
        action_verbs_score = self._analyze_action_verbs(resume_data)

        # Role alignment
        role_alignment = self._analyze_role_alignment(resume_data, job_data)

        # Resume length
        resume_length_score = self._analyze_resume_length(resume_data)

        # Section completeness
        section_completeness = self._analyze_section_completeness(resume_data)

        # Optimization potential
        optimization_potential = self._calculate_optimization_potential(
            keyword_coverage, action_verbs_score, section_completeness
        )

        # Detailed report
        detailed_report = {
            "keyword_coverage": {
                "score": keyword_coverage,
                "missing_keywords": missing_keywords,
                "matched_keywords": self._get_matched_keywords(resume_data, job_data),
            },
            "formatting": {
                "score": formatting_compatibility,
                "issues": self._identify_formatting_issues(resume_data),
            },
            "action_verbs": {
                "score": action_verbs_score,
                "found_verbs": self._count_action_verbs(resume_data),
            },
            "role_alignment": {
                "score": role_alignment,
                "alignment_factors": self._get_alignment_factors(resume_data, job_data),
            },
            "resume_length": {
                "score": resume_length_score,
                "word_count": self._count_words(resume_data),
            },
            "sections": {
                "score": section_completeness,
                "present_sections": self._get_present_sections(resume_data),
                "missing_sections": self._get_missing_sections(resume_data),
            },
        }

        return {
            "keyword_coverage": keyword_coverage,
            "formatting_compatibility": formatting_compatibility,
            "action_verbs_score": action_verbs_score,
            "role_alignment": role_alignment,
            "missing_keywords": missing_keywords,
            "resume_length_score": resume_length_score,
            "section_completeness": section_completeness,
            "optimization_potential": optimization_potential,
            "detailed_report": detailed_report,
        }

    def _analyze_keyword_coverage(self, resume: dict[str, Any], job: dict[str, Any]) -> tuple[int, list[str]]:
        """Analyze keyword coverage."""
        job_keywords = set(job.get("keywords", []))
        job_required = set(job.get("required_skills", []))
        job_tools = set(job.get("tools", []))
        job_frameworks = set(job.get("frameworks", []))

        all_keywords = job_keywords | job_required | job_tools | job_frameworks

        if not all_keywords:
            return 100, []

        # Extract resume text
        resume_text = self._extract_resume_text(resume).lower()

        missing = []
        matched = 0
        for keyword in all_keywords:
            if keyword.lower() in resume_text:
                matched += 1
            else:
                missing.append(keyword)

        coverage = int((matched / len(all_keywords)) * 100)
        return coverage, missing

    def _analyze_formatting(self, resume: dict[str, Any]) -> int:
        """Analyze formatting compatibility."""
        score = 85  # Base score for structured data

        # Check for proper sections
        if resume.get("experience"):
            score += 5
        if resume.get("education"):
            score += 5
        if resume.get("skills"):
            score += 5

        return min(score, 100)

    def _analyze_action_verbs(self, resume: dict[str, Any]) -> int:
        """Analyze action verb usage."""
        action_verbs = [
            "led",
            "developed",
            "implemented",
            "created",
            "managed",
            "designed",
            "built",
            "launched",
            "increased",
            "reduced",
            "improved",
            "achieved",
            "delivered",
            "optimized",
            "spearheaded",
        ]

        resume_text = self._extract_resume_text(resume).lower()
        verb_count = sum(1 for verb in action_verbs if verb in resume_text)

        # Estimate total bullet points based on experience
        experience_count = len(resume.get("experience", []))
        project_count = len(resume.get("projects", []))
        total_bullets = (experience_count + project_count) * 3  # Assume 3 bullets per item

        if total_bullets == 0:
            return 50

        score = int((verb_count / total_bullets) * 100)
        return min(score, 100)

    def _analyze_role_alignment(self, resume: dict[str, Any], job: dict[str, Any]) -> int:
        """Analyze role alignment."""
        job_title = job.get("title", "").lower()
        resume_titles = [exp.get("title", "").lower() for exp in resume.get("experience", [])]

        if not job_title:
            return 100

        # Check for title similarity
        title_words = set(job_title.split())
        alignment_score = 0

        for resume_title in resume_titles:
            resume_words = set(resume_title.split())
            overlap = len(title_words & resume_words)
            if overlap >= 2:
                alignment_score = max(alignment_score, 80)
            elif overlap == 1:
                alignment_score = max(alignment_score, 60)

        return alignment_score if alignment_score > 0 else 40

    def _analyze_resume_length(self, resume: dict[str, Any]) -> int:
        """Analyze resume length."""
        word_count = self._count_words(resume)

        # Ideal range: 400-800 words
        if 400 <= word_count <= 800:
            return 100
        elif 300 <= word_count < 400:
            return 85
        elif 800 < word_count <= 1000:
            return 85
        elif word_count < 300:
            return 60
        else:
            return 50

    def _analyze_section_completeness(self, resume: dict[str, Any]) -> int:
        """Analyze section completeness."""
        required_sections = ["experience", "education", "skills"]
        optional_sections = ["projects", "certifications", "achievements"]

        score = 0
        for section in required_sections:
            if resume.get(section):
                score += 30

        for section in optional_sections:
            if resume.get(section):
                score += 10

        return min(score, 100)

    def _calculate_optimization_potential(
        self, keyword_coverage: int, action_verbs: int, section_completeness: int
    ) -> int:
        """Calculate overall optimization potential."""
        # Higher score means more room for improvement
        return int((100 - keyword_coverage) * 0.4 + (100 - action_verbs) * 0.3 + (100 - section_completeness) * 0.3)

    def _extract_resume_text(self, resume: dict[str, Any]) -> str:
        """Extract all text from resume data."""
        parts = []

        if resume.get("professional_summary"):
            parts.append(resume["professional_summary"])

        for exp in resume.get("experience", []):
            parts.append(exp.get("title", ""))
            parts.append(exp.get("description", ""))
            if exp.get("achievements"):
                parts.extend(exp["achievements"])

        for proj in resume.get("projects", []):
            parts.append(proj.get("description", ""))
            parts.extend(proj.get("technologies", []))

        skills = resume.get("skills", {})
        for category in skills.values():
            parts.extend(category)

        return " ".join(parts)

    def _count_words(self, resume: dict[str, Any]) -> int:
        """Count words in resume."""
        text = self._extract_resume_text(resume)
        return len(text.split())

    def _get_matched_keywords(self, resume: dict[str, Any], job: dict[str, Any]) -> list[str]:
        """Get matched keywords."""
        job_keywords = set(job.get("keywords", []))
        job_required = set(job.get("required_skills", []))
        all_keywords = job_keywords | job_required

        resume_text = self._extract_resume_text(resume).lower()
        matched = [kw for kw in all_keywords if kw.lower() in resume_text]
        return matched

    def _identify_formatting_issues(self, resume: dict[str, Any]) -> list[str]:
        """Identify formatting issues."""
        issues = []

        if not resume.get("experience"):
            issues.append("Missing experience section")

        if not resume.get("education"):
            issues.append("Missing education section")

        if not resume.get("skills"):
            issues.append("Missing skills section")

        return issues

    def _count_action_verbs(self, resume: dict[str, Any]) -> int:
        """Count action verbs in resume."""
        action_verbs = [
            "led",
            "developed",
            "implemented",
            "created",
            "managed",
            "designed",
            "built",
            "launched",
            "increased",
            "reduced",
            "improved",
            "achieved",
            "delivered",
            "optimized",
            "spearheaded",
        ]

        resume_text = self._extract_resume_text(resume).lower()
        return sum(1 for verb in action_verbs if verb in resume_text)

    def _get_alignment_factors(self, resume: dict[str, Any], job: dict[str, Any]) -> list[str]:
        """Get alignment factors."""
        factors = []

        job_seniority = job.get("seniority", "")
        resume_years = resume.get("years_of_experience", 0)

        if job_seniority == "senior" and resume_years >= 5:
            factors.append("Experience level matches senior requirements")

        if job_seniority == "entry-level" and resume_years < 3:
            factors.append("Experience level appropriate for entry-level")

        return factors

    def _get_present_sections(self, resume: dict[str, Any]) -> list[str]:
        """Get present sections."""
        present = []
        for section in ["experience", "education", "skills", "projects", "certifications", "achievements"]:
            if resume.get(section):
                present.append(section)
        return present

    def _get_missing_sections(self, resume: dict[str, Any]) -> list[str]:
        """Get missing sections."""
        missing = []
        for section in ["experience", "education", "skills"]:
            if not resume.get(section):
                missing.append(section)
        return missing


# Global instance
ats_service = ATSService()
