"""Resume Optimization Engine service."""
import json
from typing import Any, Optional

from app.ai.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResumeOptimizer:
    """Service for optimizing resumes for specific jobs."""

    OPTIMIZATION_PROMPT = """You are an expert resume optimizer. Optimize the given resume for the target job.

IMPORTANT RULES:
- NEVER invent experience or achievements that don't exist
- Only improve wording, structure, and presentation of existing content
- Use stronger action verbs where appropriate
- Add quantification where the original suggests it but doesn't state it explicitly
- Improve ATS keyword coverage based on job requirements
- Reorder skills to prioritize relevant ones
- Highlight relevant projects
- Improve readability and recruiter appeal
- Keep factual accuracy

Return ONLY a valid JSON object with these keys:
  optimized_summary: string (improved professional summary),
  optimized_experience: list of objects with keys: original, optimized, reason, ats_improvement, recruiter_impact,
  optimized_skills: object with keys: original_order (list), optimized_order (list), reasoning (string),
  optimized_projects: list of objects with keys: original, optimized, reason, ats_improvement, recruiter_impact,
  keyword_additions: list of objects with keys: keyword, where_added, reason,
  optimization_score: number 0-100,
  estimated_ats_improvement: number 0-100 (how much ATS score improves),
  estimated_match_increase: number 0-100 (how much job match % improves),
  estimated_interview_probability: number 0-100 (estimated interview callback increase)

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
        """Initialize optimizer."""
        self.max_retries = 3

    async def optimize_resume(
        self,
        resume_data: dict[str, Any],
        job_data: dict[str, Any],
        ats_analysis: Optional[dict[str, Any]] = None,
        career_intelligence: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Optimize resume for specific job.

        Args:
            resume_data: Parsed resume data
            job_data: Job data
            ats_analysis: ATS analysis results
            career_intelligence: Career intelligence data

        Returns:
            Optimized resume with changes and metrics
        """
        await openai_client.initialize()

        for attempt in range(self.max_retries):
            try:
                response = await openai_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert resume optimizer. Return only valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": self.OPTIMIZATION_PROMPT.format(
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

                optimization = json.loads(response)
                optimization["original_resume"] = resume_data
                optimization["target_job"] = job_data
                logger.info("Resume optimization generated successfully")
                return optimization

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Resume optimization failed (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    raise

        raise RuntimeError("Failed to optimize resume after maximum retries")

    def calculate_optimization_score(self, optimization: dict[str, Any]) -> int:
        """Calculate overall optimization score.

        Args:
            optimization: Optimization results

        Returns:
            Optimization score (0-100)
        """
        score = 0

        # Experience improvements
        if optimization.get("optimized_experience"):
            exp_count = len(optimization["optimized_experience"])
            score += min(exp_count * 5, 30)

        # Project improvements
        if optimization.get("optimized_projects"):
            proj_count = len(optimization["optimized_projects"])
            score += min(proj_count * 5, 20)

        # Keyword additions
        if optimization.get("keyword_additions"):
            keyword_count = len(optimization["keyword_additions"])
            score += min(keyword_count * 3, 20)

        # Skills reordering
        if optimization.get("optimized_skills"):
            score += 10

        # Summary optimization
        if optimization.get("optimized_summary"):
            score += 20

        return min(score, 100)


# Global instance
resume_optimizer = ResumeOptimizer()
