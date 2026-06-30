"""Interview Preparation Engine service."""
import json
from typing import Any, Optional

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class InterviewPrepGenerator:
    """Service for generating interview preparation kits."""

    INTERVIEW_PREP_PROMPT = """You are an expert interview coach. Generate a comprehensive interview preparation kit.

IMPORTANT RULES:
- Personalize everything to the specific company, role, and candidate
- Include relevant technical topics based on the job requirements
- Generate behavioral questions relevant to the role
- Create STAR answer suggestions
- Include project discussion questions based on candidate's projects
- Provide coding topics if applicable
- Include system design topics if applicable
- Provide salary discussion tips
- Generate questions for the candidate to ask
- Create study plans for different timeframes
- Priority rank everything

Return ONLY a valid JSON object with this exact structure:
{
    "company_overview": string,
    "role_overview": string,
    "responsibilities": [string],
    "technical_topics": [
        {
            "topic": string,
            "priority": string,
            "resources": [string]
        }
    ],
    "behavioral_questions": [
        {
            "question": string,
            "star_suggestion": string,
            "priority": string
        }
    ],
    "project_questions": [
        {
            "question": string,
            "suggested_answer": string,
            "priority": string
        }
    ],
    "resume_questions": [
        {
            "question": string,
            "suggested_answer": string,
            "priority": string
        }
    ],
    "coding_topics": [
        {
            "topic": string,
            "priority": string,
            "practice_problems": [string]
        }
    ],
    "system_design_topics": [
        {
            "topic": string,
            "priority": string,
            "key_concepts": [string]
        }
    ],
    "hr_questions": [
        {
            "question": string,
            "suggested_answer": string
        }
    ],
    "salary_tips": [string],
    "questions_to_ask": [
        {
            "question": string,
            "reason": string
        }
    ],
    "study_plan_90min": [
        {
            "time": string,
            "task": string,
            "priority": string
        }
    ],
    "study_plan_3day": [
        {
            "day": string,
            "tasks": [string],
            "focus": string
        }
    ],
    "study_plan_7day": [
        {
            "day": string,
            "tasks": [string],
            "focus": string
        }
    ],
    "priority_ranking": {
        "highest_priority": [string],
        "high_priority": [string],
        "medium_priority": [string],
        "low_priority": [string]
    }
}

Resume Data:
{resume_data}

Job Data:
{job_data}

ATS Analysis:
{ats_analysis}

Career Intelligence:
{career_intelligence}
"""

    def __init__(self):
        """Initialize generator."""
        self.max_retries = 3

    async def generate_interview_kit(
        self,
        resume_data: dict[str, Any],
        job_data: dict[str, Any],
        ats_analysis: Optional[dict[str, Any]] = None,
        career_intelligence: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Generate comprehensive interview preparation kit.

        Args:
            resume_data: Parsed resume data
            job_data: Job data
            ats_analysis: ATS analysis results
            career_intelligence: Career intelligence data

        Returns:
            Interview preparation kit
        """
        await openai_client.initialize()

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert interview coach. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.INTERVIEW_PREP_PROMPT.format(
                                resume_data=json.dumps(resume_data, indent=2),
                                job_data=json.dumps(job_data, indent=2),
                                ats_analysis=json.dumps(ats_analysis or {}, indent=2),
                                career_intelligence=json.dumps(career_intelligence or {}, indent=2),
                            ),
                        },
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.7,
                    response_format={"type": "json_object"},
                )

                kit = json.loads(response)
                kit["company_name"] = job_data.get("company_name", "")
                kit["role_title"] = job_data.get("title", "")
                logger.info("Interview kit generated successfully")
                return kit

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Interview kit generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate interview kit after maximum retries")


# Global instance
interview_prep_generator = InterviewPrepGenerator()
