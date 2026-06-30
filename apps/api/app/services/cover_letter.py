"""Cover Letter Generation Engine service."""
import json
from typing import Any, Optional

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class CoverLetterGenerator:
    """Service for generating personalized cover letters."""

    COVER_LETTER_PROMPT = """You are an expert cover letter writer. Generate a personalized cover letter.

IMPORTANT RULES:
- Personalize to the specific company and role
- Reference the candidate's relevant experience and projects
- Align with career goals
- Use the specified tone
- Keep to the specified length
- Be authentic and professional
- Never fabricate experience

Return ONLY a valid JSON object with this exact structure:
{
    "content": string (the full cover letter),
    "personalization_points": [
        {
            "point": string,
            "source": string ("resume", "job", "career_goals")
        }
    ],
    "tone_used": string,
    "length_used": string
}

Resume Data:
{resume_data}

Job Data:
{job_data}

Career Intelligence:
{career_intelligence}

Tone: {tone}
Length: {length}
"""

    TONES = ["professional", "confident", "friendly", "executive", "technical", "startup", "enterprise"]
    LENGTHS = ["short", "medium", "long"]

    def __init__(self):
        """Initialize generator."""
        self.max_retries = 3

    async def generate_cover_letter(
        self,
        resume_data: dict[str, Any],
        job_data: dict[str, Any],
        career_intelligence: Optional[dict[str, Any]] = None,
        tone: str = "professional",
        length: str = "medium",
    ) -> dict[str, Any]:
        """Generate personalized cover letter.

        Args:
            resume_data: Parsed resume data
            job_data: Job data
            career_intelligence: Career intelligence data
            tone: Tone of the letter
            length: Length of the letter

        Returns:
            Generated cover letter with metadata
        """
        if tone not in self.TONES:
            tone = "professional"
        if length not in self.LENGTHS:
            length = "medium"

        await openai_client.initialize()

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert cover letter writer. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.COVER_LETTER_PROMPT.format(
                                resume_data=json.dumps(resume_data, indent=2),
                                job_data=json.dumps(job_data, indent=2),
                                career_intelligence=json.dumps(career_intelligence or {}, indent=2),
                                tone=tone,
                                length=length,
                            ),
                        },
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.8,
                    response_format={"type": "json_object"},
                )

                cover_letter = json.loads(response)
                cover_letter["company_name"] = job_data.get("company_name", "")
                cover_letter["role_title"] = job_data.get("title", "")
                logger.info("Cover letter generated successfully")
                return cover_letter

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Cover letter generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate cover letter after maximum retries")


# Global instance
cover_letter_generator = CoverLetterGenerator()
