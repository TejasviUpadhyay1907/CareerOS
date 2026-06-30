"""AI resume parser service using OpenAI."""
import json
from typing import Any

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIResumeParser:
    """AI-powered resume parser using OpenAI."""

    RESUME_PARSER_PROMPT = """You are an expert resume parser. Extract structured information from the following resume text.

Return ONLY a valid JSON object with this exact structure:
{
    "personal_info": {
        "name": string,
        "email": string,
        "phone": string,
        "location": string,
        "linkedin": string,
        "github": string,
        "portfolio": string
    },
    "professional_summary": string,
    "experience": [
        {
            "company": string,
            "title": string,
            "location": string,
            "start_date": string (ISO format),
            "end_date": string (ISO format or "present"),
            "is_current": boolean,
            "description": string,
            "achievements": [string]
        }
    ],
    "education": [
        {
            "institution": string,
            "degree": string,
            "field_of_study": string,
            "location": string,
            "start_date": string (ISO format),
            "end_date": string (ISO format),
            "gpa": string,
            "honors": [string]
        }
    ],
    "projects": [
        {
            "name": string,
            "description": string,
            "url": string,
            "technologies": [string],
            "achievements": [string]
        }
    ],
    "skills": {
        "technical": [string],
        "soft": [string],
        "tools": [string]
    },
    "certifications": [
        {
            "name": string,
            "issuer": string,
            "issue_date": string (ISO format),
            "expiration_date": string (ISO format),
            "credential_id": string,
            "url": string
        }
    ],
    "languages": [
        {
            "name": string,
            "proficiency": string
        }
    ],
    "achievements": [
        {
            "title": string,
            "description": string,
            "date": string (ISO format),
            "category": string
        }
    ],
    "links": [
        {
            "type": string,
            "url": string,
            "label": string
        }
    ],
    "years_of_experience": number,
    "primary_domain": string,
    "career_level": string,
    "has_leadership_experience": boolean,
    "has_open_source_contributions": boolean,
    "has_internships": boolean,
    "has_research_experience": boolean,
    "has_publications": boolean
}

Rules:
- Return ONLY the JSON, no additional text
- Use null for missing fields
- Extract dates in ISO format (YYYY-MM-DD)
- If date is not specific, use first day of month/year
- "present" for current positions
- Be thorough and extract all available information
- Handle various resume formats gracefully

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
