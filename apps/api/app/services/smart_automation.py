"""Smart Automation service for proactive recommendations."""
from typing import Any, Optional
from datetime import datetime, timedelta

from app.core.logging import get_logger

logger = get_logger(__name__)


class SmartAutomationService:
    """Service for proactive automation and recommendations."""

    def __init__(self):
        """Initialize smart automation service."""
        self.automation_rules = {
            "stale_application": {
                "threshold_days": 7,
                "action": "suggest_followup",
                "priority": "medium",
            },
            "inactive_period": {
                "threshold_days": 14,
                "action": "suggest_resume_update",
                "priority": "low",
            },
            "deadline_approaching": {
                "threshold_days": 2,
                "action": "send_reminder",
                "priority": "high",
            },
            "high_match_job": {
                "threshold_score": 85,
                "action": "recommend_application",
                "priority": "high",
            },
            "skill_gap": {
                "threshold_gap": 3,
                "action": "recommend_learning",
                "priority": "medium",
            },
        }

    async def analyze_user_activity(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """Analyze user activity and generate recommendations.

        Args:
            user_data: User activity data

        Returns:
            Analysis results with recommendations
        """
        recommendations = []

        # Check for stale applications
        stale_apps = self._find_stale_applications(user_data.get("applications", []))
        for app in stale_apps:
            recommendations.append({
                "type": "stale_application",
                "message": f"Application for {app.get('job_title')} hasn't been updated in 7+ days",
                "action": "suggest_followup",
                "priority": "medium",
                "application_id": app.get("id"),
            })

        # Check for inactive periods
        last_activity = user_data.get("last_activity_date")
        if last_activity:
            days_inactive = (datetime.now() - datetime.fromisoformat(last_activity)).days
            if days_inactive > 14:
                recommendations.append({
                    "type": "inactive_period",
                    "message": f"You haven't been active in {days_inactive} days. Consider updating your resume.",
                    "action": "suggest_resume_update",
                    "priority": "low",
                })

        # Check for approaching deadlines
        upcoming_deadlines = self._find_upcoming_deadlines(user_data.get("tasks", []))
        for task in upcoming_deadlines:
            recommendations.append({
                "type": "deadline_approaching",
                "message": f"Task '{task.get('title')}' is due in {task.get('days_until_due')} days",
                "action": "send_reminder",
                "priority": "high",
                "task_id": task.get("id"),
            })

        # Check for high-match jobs
        high_match_jobs = self._find_high_match_jobs(user_data.get("job_matches", []))
        for job in high_match_jobs:
            recommendations.append({
                "type": "high_match_job",
                "message": f"New job '{job.get('title')}' has {job.get('match_score')}% match with your profile",
                "action": "recommend_application",
                "priority": "high",
                "job_id": job.get("id"),
            })

        # Check for skill gaps
        skill_gaps = self._find_skill_gaps(user_data.get("skills", []), user_data.get("job_requirements", []))
        for gap in skill_gaps:
            recommendations.append({
                "type": "skill_gap",
                "message": f"Consider learning {gap.get('skill')} to improve your job prospects",
                "action": "recommend_learning",
                "priority": "medium",
                "skill": gap.get("skill"),
            })

        return {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat(),
        }

    def _find_stale_applications(self, applications: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Find applications that haven't been updated recently.

        Args:
            applications: List of applications

        Returns:
            List of stale applications
        """
        stale = []
        threshold = self.automation_rules["stale_application"]["threshold_days"]
        threshold_date = datetime.now() - timedelta(days=threshold)

        for app in applications:
            updated_at = app.get("updated_at")
            if updated_at:
                update_date = datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else updated_at
                if update_date < threshold_date:
                    stale.append(app)

        return stale

    def _find_upcoming_deadlines(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Find tasks with approaching deadlines.

        Args:
            tasks: List of tasks

        Returns:
            List of tasks with approaching deadlines
        """
        upcoming = []
        threshold = self.automation_rules["deadline_approaching"]["threshold_days"]
        threshold_date = datetime.now() + timedelta(days=threshold)

        for task in tasks:
            due_date = task.get("due_date")
            if due_date and task.get("status") != "completed":
                due = datetime.fromisoformat(due_date) if isinstance(due_date, str) else due_date
                if due <= threshold_date:
                    days_until = (due - datetime.now()).days
                    upcoming.append({
                        **task,
                        "days_until_due": days_until,
                    })

        return upcoming

    def _find_high_match_jobs(self, job_matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Find jobs with high match scores.

        Args:
            job_matches: List of job matches

        Returns:
            List of high-match jobs
        """
        high_match = []
        threshold = self.automation_rules["high_match_job"]["threshold_score"]

        for match in job_matches:
            if match.get("match_score", 0) >= threshold:
                high_match.append(match)

        return high_match

    def _find_skill_gaps(self, user_skills: list[str], job_requirements: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Find skill gaps between user and job requirements.

        Args:
            user_skills: List of user skills
            job_requirements: List of job requirements

        Returns:
            List of skill gaps
        """
        gaps = []
        threshold = self.automation_rules["skill_gap"]["threshold_gap"]

        skill_counts = {}
        for req in job_requirements:
            skill = req.get("skill")
            if skill and skill not in user_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1

        for skill, count in skill_counts.items():
            if count >= threshold:
                gaps.append({
                    "skill": skill,
                    "count": count,
                })

        return gaps

    async def detect_duplicate_applications(self, applications: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Detect duplicate applications to the same company.

        Args:
            applications: List of applications

        Returns:
            List of duplicate applications
        """
        company_apps = {}
        duplicates = []

        for app in applications:
            company = app.get("company_name")
            if company:
                if company not in company_apps:
                    company_apps[company] = []
                company_apps[company].append(app)

        for company, apps in company_apps.items():
            if len(apps) > 1:
                duplicates.append({
                    "company": company,
                    "applications": apps,
                    "count": len(apps),
                })

        return duplicates

    async def recommend_similar_jobs(self, application: dict[str, Any], all_jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Recommend similar jobs based on application.

        Args:
            application: Current application
            all_jobs: List of all jobs

        Returns:
            List of similar jobs
        """
        similar = []
        current_job = application.get("job", {})
        current_title = current_job.get("title", "").lower()
        current_company = current_job.get("company_name", "").lower()

        for job in all_jobs:
            job_title = job.get("title", "").lower()
            job_company = job.get("company_name", "").lower()

            # Skip same job
            if job.get("id") == current_job.get("id"):
                continue

            # Check for similar title or company
            similarity_score = 0

            # Title similarity (simple check for common words)
            title_words = set(current_title.split())
            job_title_words = set(job_title.split())
            common_words = title_words & job_title_words
            if common_words:
                similarity_score += len(common_words) * 10

            # Same company (but different role)
            if current_company == job_company and current_title != job_title:
                similarity_score += 30

            if similarity_score >= 20:
                similar.append({
                    **job,
                    "similarity_score": similarity_score,
                })

        # Sort by similarity score and return top 5
        similar.sort(key=lambda x: x["similarity_score"], reverse=True)
        return similar[:5]

    async def generate_morning_brief(self, user_data: dict[str, Any]) -> dict[str, Any]:
        """Generate morning brief for user.

        Args:
            user_data: User data

        Returns:
            Morning brief content
        """
        brief = {
            "greeting": self._get_greeting(),
            "today_priorities": [],
            "upcoming_interviews": [],
            "deadlines_today": [],
            "recommendations": [],
            "career_health": user_data.get("career_health", {}),
        }

        # Today's priorities
        pending_tasks = [t for t in user_data.get("tasks", []) if t.get("status") == "pending"]
        for task in pending_tasks[:5]:
            brief["today_priorities"].append({
                "title": task.get("title"),
                "priority": task.get("priority"),
                "estimated_time": task.get("estimated_time", "30 min"),
            })

        # Upcoming interviews
        interviews = user_data.get("interviews", [])
        for interview in interviews:
            interview_date = datetime.fromisoformat(interview.get("date")) if isinstance(interview.get("date"), str) else interview.get("date")
            if interview_date.date() == datetime.now().date():
                brief["upcoming_interviews"].append(interview)

        # Deadlines today
        for task in pending_tasks:
            due_date = datetime.fromisoformat(task.get("due_date")) if isinstance(task.get("due_date"), str) else task.get("due_date")
            if due_date.date() == datetime.now().date():
                brief["deadlines_today"].append(task)

        # AI recommendations
        analysis = await self.analyze_user_activity(user_data)
        brief["recommendations"] = analysis["recommendations"][:3]

        return brief

    def _get_greeting(self) -> str:
        """Get time-appropriate greeting.

        Returns:
            Greeting string
        """
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"


# Global instance
smart_automation_service = SmartAutomationService()
