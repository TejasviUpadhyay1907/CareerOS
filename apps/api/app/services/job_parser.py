"""AI job parser service using OpenAI."""
import json
from typing import Any

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIJobParser:
    """AI-powered job parser using OpenAI."""

    JOB_PARSER_PROMPT = """You are an expert job description parser. Extract structured information from the following job description.

Return ONLY a valid JSON object with this exact structure:
{
    "company_name": string,
    "title": string,
    "department": string,
    "employment_type": string (full-time, part-time, contract, internship),
    "location": string,
    "remote_status": string (remote, hybrid, on-site),
    "experience_required": string (e.g., "3-5 years", "5+ years"),
    "education_required": string (e.g., "Bachelor's", "Master's"),
    "salary_min": number,
    "salary_max": number,
    "salary_currency": string,
    "industry": string,
    "domain": string,
    "seniority": string (entry-level, mid-level, senior, lead, principal),
    "required_skills": [string],
    "preferred_skills": [string],
    "tools": [string],
    "frameworks": [string],
    "programming_languages": [string],
    "soft_skills": [string],
    "responsibilities": [string],
    "requirements": [string],
    "benefits": [string],
    "keywords": [string],
    "leadership_required": boolean,
    "hiring_signals": [string],
    "urgency": string (low, medium, high, urgent),
    "communication_level": string (basic, intermediate, advanced, expert),
    "team_size": string (small, medium, large, enterprise),
    "growth_potential": string (low, medium, high),
    "work_life_balance": string (poor, average, good, excellent),
    "company_culture_indicators": [string],
    "hidden_expectations": [string]
}

Rules:
- Return ONLY the JSON, no additional text
- Use null for missing fields
- Extract salary numbers as integers (no currency symbols)
- Be thorough and extract all available information
- Handle various job description formats gracefully
- Identify implicit requirements from context

Job description:
"""

    def __init__(self):
        """Initialize AI job parser."""
        self.max_retries = 3

    async def parse_job(self, job_description: str) -> dict[str, Any]:
        """Parse job description using AI.

        Args:
            job_description: Raw job description text

        Returns:
            Structured job data as dictionary
        """
        await openai_client.initialize()

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert job description parser. Return only valid JSON.",
                        },
                        {"role": "user", "content": self.JOB_PARSER_PROMPT + job_description},
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.1,
                    response_format={"type": "json_object"},
                )

                parsed_data = json.loads(response)
                logger.info("Job parsed successfully")
                return self.validate_and_normalize(parsed_data)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"AI job parsing failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to parse job description after maximum retries")

    def validate_and_normalize(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize parsed job data.

        Args:
            data: Raw parsed data

        Returns:
            Validated and normalized data
        """
        normalized = {
            "company_name": data.get("company_name") or "Unknown Company",
            "title": data.get("title") or "Unknown Role",
            "department": data.get("department") or "",
            "employment_type": data.get("employment_type") or "full-time",
            "location": data.get("location") or "",
            "remote_status": data.get("remote_status") or "on-site",
            "experience_required": data.get("experience_required") or "",
            "education_required": data.get("education_required") or "",
            "salary_min": data.get("salary_min"),
            "salary_max": data.get("salary_max"),
            "salary_currency": data.get("salary_currency") or "USD",
            "industry": data.get("industry") or "",
            "domain": data.get("domain") or "",
            "seniority": data.get("seniority") or "mid-level",
            "required_skills": data.get("required_skills") or [],
            "preferred_skills": data.get("preferred_skills") or [],
            "tools": data.get("tools") or [],
            "frameworks": data.get("frameworks") or [],
            "programming_languages": data.get("programming_languages") or [],
            "soft_skills": data.get("soft_skills") or [],
            "responsibilities": data.get("responsibilities") or [],
            "requirements": data.get("requirements") or [],
            "benefits": data.get("benefits") or [],
            "keywords": data.get("keywords") or [],
            "leadership_required": bool(data.get("leadership_required", False)),
            "hiring_signals": data.get("hiring_signals") or [],
            "urgency": data.get("urgency") or "medium",
            "communication_level": data.get("communication_level") or "intermediate",
            "team_size": data.get("team_size") or "medium",
            "growth_potential": data.get("growth_potential") or "medium",
            "work_life_balance": data.get("work_life_balance") or "average",
            "company_culture_indicators": data.get("company_culture_indicators") or [],
            "hidden_expectations": data.get("hidden_expectations") or [],
        }

        return normalized


# Global instance
ai_job_parser = AIJobParser()
