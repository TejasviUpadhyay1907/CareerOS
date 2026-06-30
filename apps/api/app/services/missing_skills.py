"""Missing skills analysis service."""
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class MissingSkillsEngine:
    """Service for analyzing missing skills from job requirements."""

    def analyze_missing_skills(
        self, resume_data: dict[str, Any], job_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Analyze missing skills from job requirements.

        Args:
            resume_data: Parsed resume data
            job_data: Parsed job data

        Returns:
            List of missing skills with metadata
        """
        missing_skills = []

        # Get resume skills
        resume_skills = set()
        if resume_data.get("skills"):
            resume_skills.update(resume_data["skills"].get("technical", []))
            resume_skills.update(resume_data["skills"].get("tools", []))
            resume_skills.update(resume_data["skills"].get("soft", []))

        # Get job skills
        job_required = job_data.get("required_skills", [])
        job_preferred = job_data.get("preferred_skills", [])
        job_tools = job_data.get("tools", [])
        job_frameworks = job_data.get("frameworks", [])
        job_languages = job_data.get("programming_languages", [])

        # Analyze required skills
        for skill in job_required:
            if skill.lower() not in [s.lower() for s in resume_skills]:
                missing_skills.append(
                    {
                        "skill_name": skill,
                        "category": "critical",
                        "learning_priority": "high",
                        "estimated_learning_time": self._estimate_learning_time(skill),
                        "difficulty": self._estimate_difficulty(skill),
                        "free_resources": self._get_learning_resources(skill),
                    }
                )

        # Analyze preferred skills
        for skill in job_preferred:
            if skill.lower() not in [s.lower() for s in resume_skills]:
                missing_skills.append(
                    {
                        "skill_name": skill,
                        "category": "recommended",
                        "learning_priority": "medium",
                        "estimated_learning_time": self._estimate_learning_time(skill),
                        "difficulty": self._estimate_difficulty(skill),
                        "free_resources": self._get_learning_resources(skill),
                    }
                )

        # Analyze tools and frameworks
        for skill in job_tools + job_frameworks + job_languages:
            if skill.lower() not in [s.lower() for s in resume_skills]:
                missing_skills.append(
                    {
                        "skill_name": skill,
                        "category": "bonus",
                        "learning_priority": "low",
                        "estimated_learning_time": self._estimate_learning_time(skill),
                        "difficulty": self._estimate_difficulty(skill),
                        "free_resources": self._get_learning_resources(skill),
                    }
                )

        logger.info(f"Identified {len(missing_skills)} missing skills")
        return missing_skills

    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate learning time for a skill.

        Args:
            skill: Skill name

        Returns:
            Estimated learning time string
        """
        skill_lower = skill.lower()

        # Frameworks and complex technologies
        if any(
            fw in skill_lower
            for fw in ["react", "angular", "vue", "django", "rails", "spring", "kubernetes"]
        ):
            return "2-3 months"

        # Programming languages
        if any(lang in skill_lower for lang in ["python", "javascript", "java", "go", "rust"]):
            return "1-2 months"

        # Tools and utilities
        if any(tool in skill_lower for tool in ["docker", "git", "jenkins", "aws", "gcp"]):
            return "2-4 weeks"

        # Soft skills
        if any(soft in skill_lower for soft in ["communication", "leadership", "teamwork"]):
            return "3-6 months"

        # Default
        return "1-2 months"

    def _estimate_difficulty(self, skill: str) -> str:
        """Estimate difficulty level for a skill.

        Args:
            skill: Skill name

        Returns:
            Difficulty level string
        """
        skill_lower = skill.lower()

        # High difficulty
        if any(
            hard in skill_lower
            for hard in ["machine learning", "kubernetes", "rust", "distributed systems", "architecture"]
        ):
            return "hard"

        # Medium difficulty
        if any(
            med in skill_lower
            for med in ["react", "angular", "django", "aws", "gcp", "python", "java"]
        ):
            return "medium"

        # Low difficulty
        if any(easy in skill_lower for easy in ["git", "docker", "sql", "html", "css"]):
            return "easy"

        return "medium"

    def _get_learning_resources(self, skill: str) -> list[str]:
        """Get free learning resources for a skill.

        Args:
            skill: Skill name

        Returns:
            List of resource names
        """
        skill_lower = skill.lower()

        resources = []

        # General resources
        resources.append("YouTube tutorials")
        resources.append("FreeCodeCamp")
        resources.append("Coursera (audit)")
        resources.append("edX (audit)")
        resources.append("Official documentation")

        # Skill-specific resources
        if "python" in skill_lower:
            resources.extend(["Python.org tutorials", "Real Python"])
        elif "javascript" in skill_lower:
            resources.extend(["MDN Web Docs", "JavaScript.info"])
        elif "react" in skill_lower:
            resources.extend(["React docs", "React Tutorial"])
        elif "aws" in skill_lower:
            resources.extend(["AWS Training", "AWS Free Tier"])

        return resources[:5]  # Return top 5 resources


# Global instance
missing_skills_engine = MissingSkillsEngine()
