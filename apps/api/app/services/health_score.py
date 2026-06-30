"""Health score calculation service for resumes."""
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class HealthScoreService:
    """Service for calculating resume health scores."""

    def calculate_health_score(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate comprehensive health score for a resume.

        Args:
            parsed_data: Parsed resume data

        Returns:
            Dictionary with health score and breakdown
        """
        breakdown = {
            "formatting": self._calculate_formatting_score(parsed_data),
            "readability": self._calculate_readability_score(parsed_data),
            "action_verbs": self._calculate_action_verbs_score(parsed_data),
            "quantified_impact": self._calculate_quantified_impact_score(parsed_data),
            "skills_coverage": self._calculate_skills_coverage_score(parsed_data),
            "project_quality": self._calculate_project_quality_score(parsed_data),
            "experience_quality": self._calculate_experience_quality_score(parsed_data),
            "education": self._calculate_education_score(parsed_data),
            "ats_friendliness": self._calculate_ats_score(parsed_data),
            "completeness": self._calculate_completeness_score(parsed_data),
        }

        overall_score = int(sum(breakdown.values()) / len(breakdown))

        recommendations = self._generate_recommendations(breakdown, parsed_data)
        strengths = self._identify_strengths(breakdown, parsed_data)
        weaknesses = self._identify_weaknesses(breakdown, parsed_data)
        missing_sections = self._identify_missing_sections(parsed_data)

        return {
            "health_score": overall_score,
            "health_breakdown": breakdown,
            "recommendations": recommendations,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_sections": missing_sections,
            "ats_score": breakdown["ats_friendliness"],
            "formatting_score": breakdown["formatting"],
            "readability_score": breakdown["readability"],
        }

    def _calculate_formatting_score(self, data: dict[str, Any]) -> int:
        """Calculate formatting score."""
        score = 85  # Base score

        # Check for structured sections
        if data.get("experience"):
            score += 5
        if data.get("education"):
            score += 5
        if data.get("skills"):
            score += 5

        return min(score, 100)

    def _calculate_readability_score(self, data: dict[str, Any]) -> int:
        """Calculate readability score."""
        score = 80  # Base score

        # Check for professional summary
        if data.get("professional_summary") and len(data["professional_summary"]) > 50:
            score += 10

        # Check for bullet points in experience
        experience = data.get("experience", [])
        if experience and any(exp.get("achievements") for exp in experience):
            score += 10

        return min(score, 100)

    def _calculate_action_verbs_score(self, data: dict[str, Any]) -> int:
        """Calculate action verbs score."""
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

        experience = data.get("experience", [])
        projects = data.get("projects", [])

        total_descriptions = []
        for exp in experience:
            if exp.get("description"):
                total_descriptions.append(exp["description"])
            if exp.get("achievements"):
                achievements = exp["achievements"]
                if isinstance(achievements, list):
                    total_descriptions.extend([str(a) for a in achievements])
                elif isinstance(achievements, str):
                    total_descriptions.append(achievements)

        for proj in projects:
            if proj.get("description"):
                total_descriptions.append(proj["description"])
            if proj.get("achievements"):
                achievements = proj["achievements"]
                if isinstance(achievements, list):
                    total_descriptions.extend([str(a) for a in achievements])
                elif isinstance(achievements, str):
                    total_descriptions.append(achievements)

        if not total_descriptions:
            return 50

        text = " ".join(total_descriptions).lower()
        verb_count = sum(1 for verb in action_verbs if verb in text)

        score = int((verb_count / max(len(total_descriptions), 1)) * 100)
        return min(score, 100)

    def _calculate_quantified_impact_score(self, data: dict[str, Any]) -> int:
        """Calculate quantified impact score."""
        experience = data.get("experience", [])
        projects = data.get("projects", [])

        total_items = len(experience) + len(projects)
        if total_items == 0:
            return 50

        quantified_count = 0

        for exp in experience:
            desc = (exp.get("description") or "")
            achievements = exp.get("achievements") or []
            if isinstance(achievements, list):
                desc += " ".join(str(a) for a in achievements)
            elif isinstance(achievements, str):
                desc += achievements
            if any(char.isdigit() for char in desc):
                quantified_count += 1

        for proj in projects:
            desc = (proj.get("description") or "")
            achievements = proj.get("achievements") or []
            if isinstance(achievements, list):
                desc += " ".join(str(a) for a in achievements)
            elif isinstance(achievements, str):
                desc += achievements
            if any(char.isdigit() for char in desc):
                quantified_count += 1

        score = int((quantified_count / total_items) * 100)
        return min(score, 100)

    def _calculate_skills_coverage_score(self, data: dict[str, Any]) -> int:
        """Calculate skills coverage score."""
        skills = data.get("skills") or {}
        if isinstance(skills, list):
            # AI may return skills as a flat list
            total_skills = len(skills)
        else:
            technical = len(skills.get("technical") or [])
            soft      = len(skills.get("soft") or [])
            tools     = len(skills.get("tools") or [])
            total_skills = technical + soft + tools

        if total_skills >= 15:
            return 100
        elif total_skills >= 10:
            return 85
        elif total_skills >= 5:
            return 70
        elif total_skills >= 3:
            return 55
        else:
            return 40

    def _calculate_project_quality_score(self, data: dict[str, Any]) -> int:
        """Calculate project quality score."""
        projects = data.get("projects", [])

        if not projects:
            return 50

        score = 60  # Base score for having projects

        for proj in projects:
            if proj.get("technologies"):
                score += 5
            if proj.get("description") and len(proj["description"]) > 50:
                score += 5
            if proj.get("achievements"):
                score += 5
            if proj.get("url"):
                score += 5

        return min(score, 100)

    def _calculate_experience_quality_score(self, data: dict[str, Any]) -> int:
        """Calculate experience quality score."""
        experience = data.get("experience", [])

        if not experience:
            return 50

        score = 60  # Base score for having experience

        for exp in experience:
            if exp.get("company") and exp.get("title"):
                score += 5
            if exp.get("achievements"):
                score += 5
            if exp.get("description") and len(exp["description"]) > 50:
                score += 5

        return min(score, 100)

    def _calculate_education_score(self, data: dict[str, Any]) -> int:
        """Calculate education score."""
        education = data.get("education", [])

        if not education:
            return 50

        score = 70  # Base score for having education

        for edu in education:
            if edu.get("institution") and edu.get("degree"):
                score += 10
            if edu.get("field_of_study"):
                score += 5
            if edu.get("gpa"):
                score += 5

        return min(score, 100)

    def _calculate_ats_score(self, data: dict[str, Any]) -> int:
        """Calculate ATS friendliness score."""
        score = 70  # Base score

        # Check for standard sections
        if data.get("experience"):
            score += 10
        if data.get("education"):
            score += 10
        if data.get("skills"):
            score += 10

        return min(score, 100)

    def _calculate_completeness_score(self, data: dict[str, Any]) -> int:
        """Calculate completeness score."""
        required_fields = [
            "personal_info",
            "experience",
            "education",
            "skills",
        ]

        optional_fields = [
            "projects",
            "certifications",
            "achievements",
            "languages",
        ]

        score = 0

        # Required fields (70% of score)
        for field in required_fields:
            if data.get(field):
                score += 17.5

        # Optional fields (30% of score)
        for field in optional_fields:
            if data.get(field):
                score += 7.5

        return int(score)

    def _generate_recommendations(
        self, breakdown: dict[str, int], data: dict[str, Any]
    ) -> list[str]:
        """Generate improvement recommendations."""
        recommendations = []

        if breakdown["quantified_impact"] < 70:
            recommendations.append("Add more quantified achievements (e.g., 'Increased revenue by 25%')")

        if breakdown["action_verbs"] < 70:
            recommendations.append("Use more action verbs to describe your experience")

        if breakdown["skills_coverage"] < 70:
            recommendations.append("Expand your skills section with more technical and soft skills")

        if breakdown["project_quality"] < 70:
            recommendations.append("Add more details to your projects, including technologies used")

        if breakdown["completeness"] < 80:
            recommendations.append("Complete missing sections like certifications or achievements")

        if not data.get("professional_summary"):
            recommendations.append("Add a professional summary to introduce yourself")

        return recommendations[:5]  # Return top 5 recommendations

    def _identify_strengths(self, breakdown: dict[str, int], data: dict[str, Any]) -> list[str]:
        """Identify resume strengths."""
        strengths = []

        if breakdown["experience_quality"] >= 80:
            strengths.append("Strong work experience with detailed descriptions")

        if breakdown["skills_coverage"] >= 80:
            strengths.append("Comprehensive skills coverage")

        if breakdown["project_quality"] >= 80:
            strengths.append("High-quality project portfolio")

        if breakdown["education"] >= 80:
            strengths.append("Strong educational background")

        if breakdown["quantified_impact"] >= 80:
            strengths.append("Excellent use of quantified achievements")

        if data.get("has_leadership_experience"):
            strengths.append("Demonstrated leadership experience")

        if data.get("has_open_source_contributions"):
            strengths.append("Open source contributions")

        return strengths[:5]

    def _identify_weaknesses(self, breakdown: dict[str, int], data: dict[str, Any]) -> list[str]:
        """Identify resume weaknesses."""
        weaknesses = []

        if breakdown["quantified_impact"] < 60:
            weaknesses.append("Lack of quantified achievements")

        if breakdown["skills_coverage"] < 60:
            weaknesses.append("Limited skills coverage")

        if breakdown["project_quality"] < 60:
            weaknesses.append("Projects need more detail")

        if not data.get("certifications"):
            weaknesses.append("No certifications listed")

        if not data.get("projects"):
            weaknesses.append("No projects showcased")

        if breakdown["completeness"] < 70:
            weaknesses.append("Missing key resume sections")

        return weaknesses[:5]

    def _identify_missing_sections(self, data: dict[str, Any]) -> list[str]:
        """Identify missing resume sections."""
        missing = []

        if not data.get("experience"):
            missing.append("Work Experience")

        if not data.get("education"):
            missing.append("Education")

        if not data.get("skills") or (
            isinstance(data["skills"], dict) and not any((v or []) for v in data["skills"].values())
        ):
            missing.append("Skills")

        if not data.get("projects"):
            missing.append("Projects")

        if not data.get("certifications"):
            missing.append("Certifications")

        if not data.get("professional_summary"):
            missing.append("Professional Summary")

        return missing


# Global instance
health_score_service = HealthScoreService()
