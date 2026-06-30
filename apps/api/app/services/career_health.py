"""Career Health Score service."""
from typing import Any, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class CareerHealthService:
    """Service for calculating career health scores."""

    def calculate_health_score(
        self,
        resume_data: Optional[dict[str, Any]] = None,
        job_matches: Optional[list[dict[str, Any]]] = None,
        ats_scores: Optional[list[int]] = None,
        skills: Optional[dict[str, Any]] = None,
        projects: Optional[list[dict[str, Any]]] = None,
        application_activity: Optional[dict[str, Any]] = None,
        career_goals: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Calculate comprehensive career health score.

        Args:
            resume_data: Parsed resume data
            job_matches: List of job match results
            ats_scores: List of ATS scores
            skills: Skills data
            projects: Projects data
            application_activity: Application activity metrics
            career_goals: Career goals

        Returns:
            Health score with breakdown
        """
        breakdown = {}

        # Resume Quality (15%)
        resume_quality, resume_reasoning = self._calculate_resume_quality(resume_data)
        breakdown["resume_quality"] = {
            "score": resume_quality,
            "weight": 15,
            "reasoning": resume_reasoning,
        }

        # Job Match Quality (15%)
        job_match_quality, match_reasoning = self._calculate_job_match_quality(job_matches)
        breakdown["job_match_quality"] = {
            "score": job_match_quality,
            "weight": 15,
            "reasoning": match_reasoning,
        }

        # ATS Performance (10%)
        ats_performance, ats_reasoning = self._calculate_ats_performance(ats_scores)
        breakdown["ats_performance"] = {
            "score": ats_performance,
            "weight": 10,
            "reasoning": ats_reasoning,
        }

        # Skill Coverage (15%)
        skill_coverage, skill_reasoning = self._calculate_skill_coverage(skills)
        breakdown["skill_coverage"] = {
            "score": skill_coverage,
            "weight": 15,
            "reasoning": skill_reasoning,
        }

        # Project Strength (10%)
        project_strength, project_reasoning = self._calculate_project_strength(projects)
        breakdown["project_strength"] = {
            "score": project_strength,
            "weight": 10,
            "reasoning": project_reasoning,
        }

        # Application Activity (10%)
        application_activity_score, activity_reasoning = self._calculate_application_activity(
            application_activity
        )
        breakdown["application_activity"] = {
            "score": application_activity_score,
            "weight": 10,
            "reasoning": activity_reasoning,
        }

        # Interview Readiness (10%)
        interview_readiness, interview_reasoning = self._calculate_interview_readiness(
            resume_data, skills, projects
        )
        breakdown["interview_readiness"] = {
            "score": interview_readiness,
            "weight": 10,
            "reasoning": interview_reasoning,
        }

        # Career Direction (5%)
        career_direction, direction_reasoning = self._calculate_career_direction(career_goals, resume_data)
        breakdown["career_direction"] = {
            "score": career_direction,
            "weight": 5,
            "reasoning": direction_reasoning,
        }

        # Consistency (5%)
        consistency, consistency_reasoning = self._calculate_consistency(
            application_activity, job_matches
        )
        breakdown["consistency"] = {
            "score": consistency,
            "weight": 5,
            "reasoning": consistency_reasoning,
        }

        # Growth Potential (5%)
        growth_potential, growth_reasoning = self._calculate_growth_potential(
            skills, projects, career_goals
        )
        breakdown["growth_potential"] = {
            "score": growth_potential,
            "weight": 5,
            "reasoning": growth_reasoning,
        }

        # Calculate overall score
        overall_score = int(
            sum(item["score"] * item["weight"] / 100 for item in breakdown.values())
        )

        return {
            "overall_score": overall_score,
            "breakdown": breakdown,
            "grade": self._get_grade(overall_score),
            "trend": "stable",  # Would be calculated from historical data
        }

    def _calculate_resume_quality(self, resume_data: Optional[dict[str, Any]]) -> tuple[int, str]:
        """Calculate resume quality score."""
        if not resume_data:
            return 0, "No resume data available"

        score = 0
        reasons = []

        # Check for key sections
        if resume_data.get("experience"):
            score += 25
            reasons.append("Has experience section")
        else:
            reasons.append("Missing experience section")

        if resume_data.get("education"):
            score += 20
            reasons.append("Has education section")
        else:
            reasons.append("Missing education section")

        if resume_data.get("skills"):
            score += 20
            reasons.append("Has skills section")
        else:
            reasons.append("Missing skills section")

        if resume_data.get("projects"):
            score += 20
            reasons.append("Has projects section")
        else:
            reasons.append("Missing projects section")

        if resume_data.get("achievements"):
            score += 15
            reasons.append("Has achievements section")
        else:
            reasons.append("Missing achievements section")

        return score, "; ".join(reasons)

    def _calculate_job_match_quality(self, job_matches: Optional[list[dict[str, Any]]]) -> tuple[int, str]:
        """Calculate job match quality score."""
        if not job_matches or len(job_matches) == 0:
            return 0, "No job matches to analyze"

        avg_match = sum(match.get("overall_match", 0) for match in job_matches) / len(job_matches)
        reasons = []

        if avg_match >= 80:
            reasons.append("Excellent average match score")
        elif avg_match >= 60:
            reasons.append("Good average match score")
        elif avg_match >= 40:
            reasons.append("Moderate average match score")
        else:
            reasons.append("Low average match score")

        reasons.append(f"Based on {len(job_matches)} job analyses")

        return int(avg_match), "; ".join(reasons)

    def _calculate_ats_performance(self, ats_scores: Optional[list[int]]) -> tuple[int, str]:
        """Calculate ATS performance score."""
        if not ats_scores or len(ats_scores) == 0:
            return 0, "No ATS scores available"

        avg_ats = sum(ats_scores) / len(ats_scores)
        reasons = []

        if avg_ats >= 80:
            reasons.append("Strong ATS performance")
        elif avg_ats >= 60:
            reasons.append("Moderate ATS performance")
        else:
            reasons.append("Weak ATS performance - needs optimization")

        return int(avg_ats), "; ".join(reasons)

    def _calculate_skill_coverage(self, skills: Optional[dict[str, Any]]) -> tuple[int, str]:
        """Calculate skill coverage score."""
        if not skills:
            return 0, "No skills data available"

        score = 0
        reasons = []

        skill_categories = ["technical", "soft", "tools", "languages"]
        present_categories = sum(1 for cat in skill_categories if skills.get(cat))

        score = int((present_categories / len(skill_categories)) * 100)
        reasons.append(f"{present_categories}/{len(skill_categories)} skill categories present")

        # Check skill depth
        total_skills = sum(len(skills.get(cat, [])) for cat in skill_categories)
        if total_skills >= 20:
            reasons.append("Strong skill depth")
        elif total_skills >= 10:
            reasons.append("Moderate skill depth")
        else:
            reasons.append("Limited skill depth")

        return score, "; ".join(reasons)

    def _calculate_project_strength(self, projects: Optional[list[dict[str, Any]]]) -> tuple[int, str]:
        """Calculate project strength score."""
        if not projects:
            return 0, "No projects available"

        score = 0
        reasons = []

        # Number of projects
        if len(projects) >= 5:
            score += 40
            reasons.append("Strong project portfolio")
        elif len(projects) >= 3:
            score += 30
            reasons.append("Moderate project portfolio")
        else:
            score += 15
            reasons.append("Limited project portfolio")

        # Project quality (technologies used)
        avg_techs = sum(len(proj.get("technologies", [])) for proj in projects) / len(projects)
        if avg_techs >= 3:
            score += 30
            reasons.append("Projects use diverse technologies")
        elif avg_techs >= 2:
            score += 20
            reasons.append("Projects show some technology diversity")
        else:
            score += 10
            reasons.append("Projects lack technology diversity")

        # Project descriptions
        has_descriptions = sum(1 for proj in projects if proj.get("description"))
        if has_descriptions == len(projects):
            score += 30
            reasons.append("All projects have descriptions")
        else:
            score += 10
            reasons.append("Some projects lack descriptions")

        return score, "; ".join(reasons)

    def _calculate_application_activity(
        self, application_activity: Optional[dict[str, Any]]
    ) -> tuple[int, str]:
        """Calculate application activity score."""
        if not application_activity:
            return 0, "No application activity data"

        score = 0
        reasons = []

        # Recent applications
        recent_apps = application_activity.get("recent_applications_count", 0)
        if recent_apps >= 10:
            score += 40
            reasons.append("High application activity")
        elif recent_apps >= 5:
            score += 30
            reasons.append("Moderate application activity")
        elif recent_apps >= 1:
            score += 20
            reasons.append("Low application activity")
        else:
            score += 0
            reasons.append("No recent applications")

        # Application consistency
        consistency_days = application_activity.get("days_since_last_application", 999)
        if consistency_days <= 3:
            score += 30
            reasons.append("Consistent application pattern")
        elif consistency_days <= 7:
            score += 20
            reasons.append("Fairly consistent application pattern")
        else:
            score += 10
            reasons.append("Inconsistent application pattern")

        # Response rate
        response_rate = application_activity.get("response_rate", 0)
        if response_rate >= 0.3:
            score += 30
            reasons.append("Good response rate")
        elif response_rate >= 0.1:
            score += 20
            reasons.append("Moderate response rate")
        else:
            score += 10
            reasons.append("Low response rate")

        return score, "; ".join(reasons)

    def _calculate_interview_readiness(
        self,
        resume_data: Optional[dict[str, Any]],
        skills: Optional[dict[str, Any]],
        projects: Optional[list[dict[str, Any]]],
    ) -> tuple[int, str]:
        """Calculate interview readiness score."""
        score = 0
        reasons = []

        # Experience depth
        if resume_data and resume_data.get("years_of_experience", 0) >= 3:
            score += 30
            reasons.append("Sufficient experience for interviews")
        elif resume_data:
            score += 15
            reasons.append("Limited experience - may need preparation")
        else:
            score += 0
            reasons.append("No experience data")

        # Technical skills
        if skills and len(skills.get("technical", [])) >= 5:
            score += 30
            reasons.append("Strong technical foundation")
        elif skills:
            score += 15
            reasons.append("Basic technical foundation")
        else:
            score += 0
            reasons.append("No technical skills data")

        # Project examples
        if projects and len(projects) >= 3:
            score += 40
            reasons.append("Good project examples to discuss")
        elif projects:
            score += 20
            reasons.append("Some project examples available")
        else:
            score += 0
            reasons.append("No project examples for interviews")

        return score, "; ".join(reasons)

    def _calculate_career_direction(
        self, career_goals: Optional[list[dict[str, Any]]], resume_data: Optional[dict[str, Any]]
    ) -> tuple[int, str]:
        """Calculate career direction score."""
        score = 0
        reasons = []

        # Has career goals
        if career_goals and len(career_goals) > 0:
            score += 40
            reasons.append("Has defined career goals")
        else:
            score += 0
            reasons.append("No career goals defined")

        # Goal progress
        if career_goals:
            avg_progress = sum(goal.get("progress", 0) for goal in career_goals) / len(career_goals)
            if avg_progress >= 50:
                score += 30
                reasons.append("Good progress toward goals")
            elif avg_progress >= 25:
                score += 20
                reasons.append("Some progress toward goals")
            else:
                score += 10
                reasons.append("Limited progress toward goals")

        # Resume alignment with direction
        if resume_data and resume_data.get("primary_domain"):
            score += 30
            reasons.append("Resume shows clear direction")
        else:
            score += 10
            reasons.append("Resume lacks clear direction")

        return score, "; ".join(reasons)

    def _calculate_consistency(
        self, application_activity: Optional[dict[str, Any]], job_matches: Optional[list[dict[str, Any]]]
    ) -> tuple[int, str]:
        """Calculate consistency score."""
        score = 0
        reasons = []

        # Application consistency
        if application_activity:
            days_since_last = application_activity.get("days_since_last_application", 999)
            if days_since_last <= 7:
                score += 50
                reasons.append("Consistent application activity")
            elif days_since_last <= 14:
                score += 30
                reasons.append("Fairly consistent activity")
            else:
                score += 10
                reasons.append("Inconsistent activity pattern")
        else:
            score += 0
            reasons.append("No activity data")

        # Target consistency
        if job_matches and len(job_matches) > 0:
            roles = [match.get("job_title", "") for match in job_matches]
            # Check if targeting similar roles
            unique_roles = len(set(roles))
            if unique_roles <= 2:
                score += 50
                reasons.append("Focused on specific role types")
            else:
                score += 30
                reasons.append("Broad targeting - consider focusing")
        else:
            score += 20
            reasons.append("No job match data")

        return score, "; ".join(reasons)

    def _calculate_growth_potential(
        self,
        skills: Optional[dict[str, Any]],
        projects: Optional[list[dict[str, Any]]],
        career_goals: Optional[list[dict[str, Any]]],
    ) -> tuple[int, str]:
        """Calculate growth potential score."""
        score = 0
        reasons = []

        # Learning indicators
        if skills:
            total_skills = sum(len(skills.get(cat, [])) for cat in ["technical", "tools", "languages"])
            if total_skills >= 15:
                score += 40
                reasons.append("Strong skill foundation for growth")
            elif total_skills >= 8:
                score += 30
                reasons.append("Moderate skill foundation")
            else:
                score += 15
                reasons.append("Limited skill foundation")
        else:
            score += 0
            reasons.append("No skills data")

        # Project diversity
        if projects and len(projects) >= 3:
            score += 30
            reasons.append("Diverse project experience")
        elif projects:
            score += 15
            reasons.append("Limited project diversity")
        else:
            score += 0
            reasons.append("No project data")

        # Goal ambition
        if career_goals and len(career_goals) >= 2:
            score += 30
            reasons.append("Ambitious career goals")
        elif career_goals:
            score += 15
            reasons.append("Some career goals")
        else:
            score += 0
            reasons.append("No career goals")

        return score, "; ".join(reasons)

    def _get_grade(self, score: int) -> str:
        """Get letter grade for score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


# Global instance
career_health_service = CareerHealthService()
