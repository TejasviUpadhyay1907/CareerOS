"""AI insights generation service using OpenAI."""
import json
from typing import Any

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class InsightsService:
    """AI-powered insights generation service."""

    INSIGHTS_PROMPT = """You are an expert career advisor and recruiter. Generate personalized insights for a candidate applying to a job.

Return ONLY a valid JSON object with this exact structure:
{{
    "top_strengths": [list of strings - top 5 strengths for this specific role],
    "biggest_weaknesses": [list of strings - top 5 weaknesses for this specific role],
    "reasons_recruiter_may_reject": [list of strings - potential rejection reasons],
    "reasons_recruiter_may_shortlist": [list of strings - potential shortlist reasons],
    "hidden_expectations": [list of strings - unspoken job requirements],
    "resume_gaps": [list of strings - gaps in resume for this role],
    "experience_gaps": [list of strings - missing experience areas],
    "suggested_resume_changes": [list of strings - specific resume improvements],
    "suggested_projects": [list of strings - project ideas to strengthen application],
    "suggested_certifications": [list of strings - certifications to pursue],
    "suggested_technologies": [list of strings - technologies to learn],
    "suggested_interview_topics": [list of strings - topics to prepare for interviews]
}}

Resume data:
{resume_summary}

Job data:
{job_summary}

Match analysis:
{match_summary}

Rules:
- Return ONLY the JSON, no additional text
- Be specific and actionable
- Tailor insights to the specific job role
- Provide realistic and practical suggestions
- Consider the match scores in your analysis
"""

    def __init__(self):
        """Initialize insights service."""
        self.max_retries = 3

    async def generate_insights(
        self, resume_data: dict[str, Any], job_data: dict[str, Any], match_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate AI-powered insights.

        Args:
            resume_data: Parsed resume data
            job_data: Parsed job data
            match_data: Match analysis data

        Returns:
            Insights as dictionary
        """
        await openai_client.initialize()

        resume_summary = self._summarize_resume(resume_data)
        job_summary = self._summarize_job(job_data)
        match_summary = self._summarize_match(match_data)

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert career advisor. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.INSIGHTS_PROMPT.format(
                                resume_summary=resume_summary,
                                job_summary=job_summary,
                                match_summary=match_summary,
                            ),
                        },
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.7,
                    response_format={"type": "json_object"},
                )

                insights = json.loads(response)
                logger.info("Insights generated successfully")
                return self.validate_insights(insights)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"AI insights generation failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate insights after maximum retries")

    def _summarize_resume(self, resume: dict[str, Any]) -> str:
        """Summarize resume data for AI."""
        parts = []

        personal = resume.get("personal_info", {})
        parts.append(f"Name: {personal.get('name', 'N/A')}")
        parts.append(f"Years of Experience: {resume.get('years_of_experience', 0)}")

        if resume.get("experience"):
            parts.append(f"\nExperience ({len(resume['experience'])} positions):")
            for exp in resume["experience"][:3]:
                parts.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")

        skills = resume.get("skills", {})
        if skills:
            parts.append("\nSkills:")
            for category, skill_list in skills.items():
                if skill_list:
                    parts.append(f"- {category}: {', '.join(skill_list[:5])}")

        return "\n".join(parts)

    def _summarize_job(self, job: dict[str, Any]) -> str:
        """Summarize job data for AI."""
        parts = []

        parts.append(f"Company: {job.get('company_name', 'N/A')}")
        parts.append(f"Role: {job.get('title', 'N/A')}")
        parts.append(f"Seniority: {job.get('seniority', 'N/A')}")
        parts.append(f"Experience Required: {job.get('experience_required', 'N/A')}")

        if job.get("required_skills"):
            parts.append(f"\nRequired Skills: {', '.join(job['required_skills'][:10])}")

        if job.get("responsibilities"):
            parts.append(f"\nResponsibilities: {', '.join(job['responsibilities'][:3])}")

        return "\n".join(parts)

    def _summarize_match(self, match: dict[str, Any]) -> str:
        """Summarize match data for AI."""
        parts = []

        parts.append(f"Overall Match: {match.get('overall_match', 0)}%")
        parts.append(f"Technical Match: {match.get('technical_match', 0)}%")
        parts.append(f"Experience Match: {match.get('experience_match', 0)}%")
        parts.append(f"Education Match: {match.get('education_match', 0)}%")
        parts.append(f"ATS Match: {match.get('ats_match', 0)}%")

        reasoning = match.get("match_reasoning", {})
        if reasoning:
            parts.append("\nMatch Reasoning:")
            for category, reason in reasoning.items():
                parts.append(f"- {category}: {reason}")

        return "\n".join(parts)

    def validate_insights(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate and normalize insights data.

        Args:
            data: Raw insights data

        Returns:
            Validated insights data
        """
        return {
            "top_strengths": data.get("top_strengths", []),
            "biggest_weaknesses": data.get("biggest_weaknesses", []),
            "reasons_recruiter_may_reject": data.get("reasons_recruiter_may_reject", []),
            "reasons_recruiter_may_shortlist": data.get("reasons_recruiter_may_shortlist", []),
            "hidden_expectations": data.get("hidden_expectations", []),
            "resume_gaps": data.get("resume_gaps", []),
            "experience_gaps": data.get("experience_gaps", []),
            "suggested_resume_changes": data.get("suggested_resume_changes", []),
            "suggested_projects": data.get("suggested_projects", []),
            "suggested_certifications": data.get("suggested_certifications", []),
            "suggested_technologies": data.get("suggested_technologies", []),
            "suggested_interview_topics": data.get("suggested_interview_topics", []),
        }


# Global instance
insights_service = InsightsService()
