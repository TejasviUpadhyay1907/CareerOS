"""AI resume parser service using OpenAI."""
import json
from typing import Any

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIResumeParser:
    """AI-powered resume parser using OpenAI."""

    RESUME_PARSER_PROMPT = """You are an expert resume parser. Extract ALL structured information from the following resume text.

IMPORTANT RULES:
- Extract EVERY project, experience, skill, certification mentioned — do not skip anything
- For years_of_experience: calculate from earliest job start date to now, or estimate from context
- For primary_domain: identify the main field (e.g., "Software Engineering", "Data Science", "Product Management", "Finance")
- For career_level: "student/fresher", "junior", "mid-level", "senior", or "lead/principal"
- If a field is not mentioned, use null (not empty string)
- For skills: separate into technical (programming languages, frameworks), soft (communication, leadership), tools (software, platforms)
- Extract ALL projects even if they are personal/academic/hackathon projects

Return ONLY a valid JSON object with this exact structure (no extra text):
{
    "personal_info": {"name": null, "email": null, "phone": null, "location": null, "linkedin": null, "github": null, "portfolio": null},
    "professional_summary": null,
    "experience": [{"company": null, "title": null, "location": null, "start_date": null, "end_date": null, "is_current": false, "description": null, "achievements": []}],
    "education": [{"institution": null, "degree": null, "field_of_study": null, "location": null, "start_date": null, "end_date": null, "gpa": null, "honors": []}],
    "projects": [{"name": null, "description": null, "url": null, "technologies": [], "achievements": []}],
    "skills": {"technical": [], "soft": [], "tools": []},
    "certifications": [{"name": null, "issuer": null, "issue_date": null, "expiration_date": null, "credential_id": null, "url": null}],
    "languages": [{"name": null, "proficiency": null}],
    "achievements": [{"title": null, "description": null, "date": null, "category": null}],
    "links": [{"type": null, "url": null, "label": null}],
    "years_of_experience": 0,
    "primary_domain": null,
    "career_level": null,
    "has_leadership_experience": false,
    "has_open_source_contributions": false,
    "has_internships": false,
    "has_research_experience": false,
    "has_publications": false
}

Resume text:
"""

    def __init__(self):
        """Initialize AI parser."""
        self.max_retries = 3

    async def parse_resume(self, resume_text: str) -> dict[str, Any]:
        """Parse resume text using AI.

        Args:
            resume_text: Raw resume text

        Returns:
            Structured resume data as dictionary
        """
        await openai_client.initialize()

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert resume parser. Return only valid JSON.",
                        },
                        {"role": "user", "content": self.RESUME_PARSER_PROMPT + resume_text},
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.1,
                    response_format={"type": "json_object"},
                )

                parsed_data = json.loads(response)
                logger.info("Resume parsed successfully")
                return self.validate_and_normalize(parsed_data)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"AI parsing failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to parse resume after maximum retries")

    def validate_and_normalize(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize parsed resume data.

        Args:
            data: Raw parsed data

        Returns:
            Validated and normalized data
        """
        # Ensure all required keys exist
        normalized = {
            "personal_info": data.get("personal_info", {}),
            "professional_summary": data.get("professional_summary", ""),
            "experience": data.get("experience", []),
            "education": data.get("education", []),
            "projects": data.get("projects", []),
            "skills": data.get("skills", {"technical": [], "soft": [], "tools": []}),
            "certifications": data.get("certifications", []),
            "languages": data.get("languages", []),
            "achievements": data.get("achievements", []),
            "links": data.get("links", []),
            "years_of_experience": data.get("years_of_experience", 0),
            "primary_domain": data.get("primary_domain", ""),
            "career_level": data.get("career_level", ""),
            "has_leadership_experience": data.get("has_leadership_experience", False),
            "has_open_source_contributions": data.get("has_open_source_contributions", False),
            "has_internships": data.get("has_internships", False),
            "has_research_experience": data.get("has_research_experience", False),
            "has_publications": data.get("has_publications", False),
        }

        return normalized


# Global instance
ai_resume_parser = AIResumeParser()
