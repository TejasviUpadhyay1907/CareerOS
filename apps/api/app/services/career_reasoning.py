"""Career AI Reasoning Engine."""
import json
from typing import Any, Optional

from app.ai.openai_client import openai_client
from app.core.logging import get_logger
from app.services.career_health import career_health_service

logger = get_logger(__name__)


class CareerReasoningEngine:
    """AI reasoning engine for career intelligence."""

    REASONING_PROMPT = """You are an expert career coach and AI reasoning engine. Analyze the user's career data and generate proactive insights.

Return ONLY a valid JSON object with this exact structure:
{
    "insights": [
        {
            "type": string (e.g., "resume_trend", "job_trend", "application_pattern", "skill_gap", "career_growth"),
            "title": string,
            "description": string,
            "severity": string (critical, high, medium, low),
            "confidence": number (0-100),
            "evidence": [string],
            "actionable": boolean
        }
    ],
    "recommendations": [
        {
            "title": string,
            "description": string,
            "category": string (immediate, this_week, this_month, long_term),
            "priority": string (critical, high, medium, low),
            "difficulty": string (easy, medium, hard),
            "estimated_time": string,
            "expected_benefit": string,
            "confidence": number (0-100),
            "evidence": [string]
        }
    ],
    "predictions": [
        {
            "type": string (ats_increase, match_increase, interview_probability, offer_probability),
            "title": string,
            "description": string,
            "predicted_value": number,
            "confidence": number (0-100),
            "time_horizon": string,
            "factors": [string]
        }
    ],
    "opportunities": [
        {
            "type": string (best_job_category, best_resume, missing_certification, high_value_project),
            "title": string,
            "description": string,
            "confidence": number (0-100),
            "evidence": [string]
        }
    ]
}

Career Data:
{career_data}

Resume Data:
{resume_data}

Job Match Data:
{job_data}

Application Data:
{application_data}

Rules:
- Return ONLY the JSON, no additional text
- Be proactive - identify issues before the user asks
- Every recommendation must cite specific evidence
- Never give generic advice
- Use confidence scores honestly
- Focus on high-impact, actionable recommendations
"""

    def __init__(self):
        """Initialize reasoning engine."""
        self.max_retries = 3

    async def generate_career_intelligence(
        self,
        career_data: dict[str, Any],
        resume_data: Optional[dict[str, Any]] = None,
        job_data: Optional[list[dict[str, Any]]] = None,
        application_data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Generate comprehensive career intelligence.

        Args:
            career_data: Career profile data
            resume_data: Resume data
            job_data: Job match data
            application_data: Application activity data

        Returns:
            Career intelligence with insights, recommendations, predictions
        """
        await openai_client.initialize()

        # Calculate health score first
        health_score = career_health_service.calculate_health_score(
            resume_data=resume_data,
            job_matches=job_data,
            application_activity=application_data,
            career_goals=career_data.get("goals", []),
        )

        # Generate AI reasoning
        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert career coach. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.REASONING_PROMPT.format(
                                career_data=json.dumps(career_data, indent=2),
                                resume_data=json.dumps(resume_data or {}, indent=2),
                                job_data=json.dumps(job_data or [], indent=2),
                                application_data=json.dumps(application_data or {}, indent=2),
                            ),
                        },
                    ],
                    model="openai/gpt-4o-mini",  # OpenRouter format
                    temperature=0.7,
                    response_format={"type": "json_object"},
                )

                intelligence = json.loads(response)
                intelligence["health_score"] = health_score
                logger.info("Career intelligence generated successfully")
                return intelligence

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"AI reasoning failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to generate career intelligence after maximum retries")

    def categorize_recommendations(self, recommendations: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Categorize recommendations by time horizon and priority.

        Args:
            recommendations: List of recommendations

        Returns:
            Categorized recommendations
        """
        categorized = {
            "immediate": [],
            "this_week": [],
            "this_month": [],
            "long_term": [],
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
        }

        for rec in recommendations:
            time_horizon = rec.get("category", "this_week")
            priority = rec.get("priority", "medium")

            if time_horizon in categorized:
                categorized[time_horizon].append(rec)
            if priority in categorized:
                categorized[priority].append(rec)

        return categorized

    def generate_todays_priorities(
        self, recommendations: list[dict[str, Any]], health_score: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Generate today's priorities from recommendations and health score.

        Args:
            recommendations: List of recommendations
            health_score: Health score data

        Returns:
            Prioritized actions for today
        """
        priorities = []

        # Get critical and high priority immediate actions
        for rec in recommendations:
            if rec.get("category") == "immediate" and rec.get("priority") in ["critical", "high"]:
                priorities.append({
                    "title": rec["title"],
                    "description": rec["description"],
                    "estimated_time": rec.get("estimated_time"),
                    "expected_benefit": rec.get("expected_benefit"),
                    "confidence": rec.get("confidence"),
                })

        # Add health score critical areas
        breakdown = health_score.get("breakdown", {})
        for category, data in breakdown.items():
            if data["score"] < 50:
                priorities.append({
                    "title": f"Improve {category.replace('_', ' ').title()}",
                    "description": data["reasoning"],
                    "estimated_time": "1-2 hours",
                    "expected_benefit": f"+{100 - data['score']} points to health score",
                    "confidence": 85,
                })

        # Sort by confidence and limit to top 5
        priorities.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return priorities[:5]


# Global instance
career_reasoning_engine = CareerReasoningEngine()
