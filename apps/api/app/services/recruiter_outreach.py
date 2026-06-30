"""Recruiter Outreach Engine service."""
import json
from typing import Any, Optional

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class RecruiterOutreachGenerator:
    """Service for generating recruiter outreach messages."""

    OUTREACH_PROMPT = """You are an expert recruiter outreach writer. Generate a personalized outreach message.

IMPORTANT RULES:
- Personalize based on the candidate's background and the company/role
- Be authentic and professional
- Include a clear call to action
- Never be generic or spammy
- Use the specified tone and length

Return ONLY a valid JSON object with this exact structure:
{
    "subject": string (if applicable),
    "content": string,
    "personalization_reason": string,
    "call_to_action": string,
    "tone_used": string,
    "length_used": string
}

Resume Data:
{resume_data}

Job Data:
{job_data}

Career Intelligence:
{career_intelligence}

Message Type: {message_type}
Tone: {tone}
Length: {length}
"""

    MESSAGE_TYPES = [
        "linkedin_connection",
        "linkedin_follow_up",
        "cold_email",
        "referral_request",
        "recruiter_follow_up",
        "hiring_manager_email",
        "thank_you_email",
        "second_follow_up",
    ]
    TONES = ["professional", "confident", "friendly", "casual", "formal"]
    LENGTHS = ["short", "medium", "long"]

    def __init__(self):
        """Initialize generator."""
        self.max_retries = 3

    async def generate_outreach(
        self,
        resume_data: dict[str, Any],
        job_data: Optional[dict[str, Any]],
        career_intelligence: Optional[dict[str, Any]] = None,
        message_type: str = "linkedin_connection",
        tone: str = "professional",
        length: str = "medium",
    ) -> dict[str, Any]:
        """Generate personalized outreach message.

        Args:
            resume_data: Parsed resume data
            job_data: Job data (optional for some message types)
            career_intelligence: Career intelligence data
            message_type: Type of message
            tone: Tone of the message
            length: Length of the message

        Returns:
            Generated outreach message with metadata
        """
        if message_type not in self.MESSAGE_TYPES:
            message_type = "linkedin_connection"
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
                            "content": "You are an expert recruiter outreach writer. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.OUTREACH_PROMPT.format(
                                resume_data=json.dumps(resume_data, indent=2),
                                job_data=json.dumps(job_data or {}, indent=2),
                                career_intelligence=json.dumps(career_intelligence or {}, indent=2),
                                message_type=message_type,
                                tone=tone,
                                length=length,
                            ),
                        },
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.8,
                    response_format={"type": "json_object"},
                )

                outreach = json.loads(response)
                outreach["message_type"] = message_type
                if job_data:
                    outreach["recipient_company"] = job_data.get("company_name", "")
                logger.info("Outreach message generated successfully")
                return outreach

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Outreach generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate outreach after maximum retries")


# Global instance
recruiter_outreach_generator = RecruiterOutreachGenerator()
