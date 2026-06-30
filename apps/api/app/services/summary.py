"""Resume summary generation service using AI."""
from typing import Any

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class SummaryService:
    """Service for generating AI-powered resume summaries."""

    SUMMARY_PROMPT = """You are an expert career advisor. Generate a comprehensive summary of the following resume data.

Return ONLY a valid JSON object with this exact structure:
{
    "professional_summary": string (2-3 sentences professional overview),
    "career_highlights": [string] (top 5 career achievements),
    "top_strengths": [string] (top 5 professional strengths),
    "potential_weaknesses": [string] (areas for improvement),
    "career_level": string (entry-level, mid-level, senior, executive),
    "primary_technology_stack": [string] (main technologies),
    "suggested_job_roles": [string] (5 relevant job titles),
    "suggested_industries": [string] (5 relevant industries),
    "top_keywords": [string] (10 important keywords for ATS)
}

Resume data:
"""

    def __init__(self):
        """Initialize summary service."""
        self.max_retries = 3

    async def generate_summary(self, parsed_data: dict[str, Any]) -> dict[str, Any]:
        """Generate AI-powered resume summary.

        Args:
            parsed_data: Parsed resume data

        Returns:
            Summary data as dictionary
        """
        await openai_client.initialize()

        # Create a text representation of the resume
        resume_text = self._format_resume_for_summary(parsed_data)

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert career advisor. Return only valid JSON.",
                        },
                        {"role": "user", "content": self.SUMMARY_PROMPT + resume_text},
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.7,
                    response_format={"type": "json_object"},
                )

                import json

                summary_data = json.loads(response)
                logger.info("Resume summary generated successfully")
                return self.validate_summary(summary_data)

            except Exception as e:
                logger.error(f"Summary generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    # Return fallback summary if AI fails
                    return self._generate_fallback_summary(parsed_data)

        raise RuntimeError("Failed to generate summary after maximum retries")

    def _format_resume_for_summary(self, data: dict[str, Any]) -> str:
        """Format resume data for AI processing.

        Args:
            data: Parsed resume data

        Returns:
            Formatted text
        """
        lines = []

        # Personal info
        personal = data.get("personal_info", {})
        lines.append(f"Name: {personal.get('name', 'N/A')}")
        lines.append(f"Email: {personal.get('email', 'N/A')}")

        # Professional summary
        if data.get("professional_summary"):
            lines.append(f"\nSummary: {data['professional_summary']}")

        # Experience
        experience = data.get("experience", [])
        if experience:
            lines.append("\nExperience:")
            for exp in experience[:5]:  # Limit to first 5
                lines.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                if exp.get("achievements"):
                    lines.append(f"  Achievements: {', '.join(exp['achievements'][:3])}")

        # Education
        education = data.get("education", [])
        if education:
            lines.append("\nEducation:")
            for edu in education[:3]:
                lines.append(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}")

        # Skills
        skills = data.get("skills", {})
        if skills:
            lines.append("\nSkills:")
            for category, skill_list in skills.items():
                if skill_list:
                    lines.append(f"- {category}: {', '.join(skill_list[:10])}")

        # Projects
        projects = data.get("projects", [])
        if projects:
            lines.append("\nProjects:")
            for proj in projects[:3]:
                lines.append(f"- {proj.get('name', 'N/A')}: {proj.get('description', 'N/A')[:100]}")

        return "\n".join(lines)

    def validate_summary(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize summary data.

        Args:
            data: Raw summary data

        Returns:
            Validated summary data
        """
        return {
            "professional_summary": data.get("professional_summary", ""),
            "career_highlights": data.get("career_highlights", []),
            "top_strengths": data.get("top_strengths", []),
            "potential_weaknesses": data.get("potential_weaknesses", []),
            "career_level": data.get("career_level", "mid-level"),
            "primary_technology_stack": data.get("primary_technology_stack", []),
            "suggested_job_roles": data.get("suggested_job_roles", []),
            "suggested_industries": data.get("suggested_industries", []),
            "top_keywords": data.get("top_keywords", []),
        }

    def _generate_fallback_summary(self, data: dict[str, Any]) -> dict[str, Any]:
        """Generate a fallback summary without AI.

        Args:
            data: Parsed resume data

        Returns:
            Fallback summary data
        """
        personal = data.get("personal_info", {})
        experience = data.get("experience", [])
        skills = data.get("skills", {})

        # Determine career level
        years_exp = data.get("years_of_experience", 0)
        if years_exp < 2:
            career_level = "entry-level"
        elif years_exp < 5:
            career_level = "mid-level"
        elif years_exp < 10:
            career_level = "senior"
        else:
            career_level = "executive"

        # Extract tech stack
        tech_stack = skills.get("technical", []) + skills.get("tools", [])

        # Generate professional summary
        name = personal.get("name", "Professional")
        title = experience[0].get("title", "Professional") if experience else "Professional"
        summary = f"{name} is a {career_level} {title} with {years_exp} years of experience."

        return {
            "professional_summary": summary,
            "career_highlights": [
                f"{years_exp} years of professional experience",
                f"{len(experience)} positions held",
                f"{len(tech_stack)} technical skills",
            ],
            "top_strengths": [
                "Professional experience",
                "Technical skills",
                "Educational background",
            ],
            "potential_weaknesses": [
                "Consider adding more quantified achievements",
                "Expand project portfolio",
            ],
            "career_level": career_level,
            "primary_technology_stack": tech_stack[:10],
            "suggested_job_roles": [title] if title else ["Software Engineer"],
            "suggested_industries": ["Technology", "Software"],
            "top_keywords": tech_stack[:10],
        }


# Global instance
summary_service = SummaryService()
