"""Export Engine service for document generation."""
from typing import Any, Optional
from datetime import datetime
import os

from app.core.logging import get_logger

logger = get_logger(__name__)


class ExportEngine:
    """Service for exporting documents in various formats."""

    def __init__(self):
        """Initialize export engine."""
        self.export_dir = "exports"

    def export_to_markdown(self, content: str, title: str) -> str:
        """Export content to Markdown format.

        Args:
            content: Content to export
            title: Document title

        Returns:
            File path of exported document
        """
        os.makedirs(self.export_dir, exist_ok=True)
        filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(content)

        logger.info(f"Exported to Markdown: {filepath}")
        return filepath

    def export_to_text(self, content: str, title: str) -> str:
        """Export content to plain text format.

        Args:
            content: Content to export
            title: Document title

        Returns:
            File path of exported document
        """
        os.makedirs(self.export_dir, exist_ok=True)
        filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write("=" * len(title) + "\n\n")
            f.write(content)

        logger.info(f"Exported to Text: {filepath}")
        return filepath

    def export_resume_to_markdown(self, resume_data: dict[str, Any]) -> str:
        """Export resume data to Markdown format.

        Args:
            resume_data: Resume data

        Returns:
            File path of exported document
        """
        md_content = self._format_resume_as_markdown(resume_data)
        return self.export_to_markdown(md_content, "Resume")

    def export_cover_letter_to_markdown(self, cover_letter: str, company_name: str) -> str:
        """Export cover letter to Markdown format.

        Args:
            cover_letter: Cover letter content
            company_name: Company name

        Returns:
            File path of exported document
        """
        return self.export_to_markdown(cover_letter, f"Cover_Letter_{company_name}")

    def export_interview_kit_to_markdown(self, kit_data: dict[str, Any]) -> str:
        """Export interview kit to Markdown format.

        Args:
            kit_data: Interview kit data

        Returns:
            File path of exported document
        """
        md_content = self._format_interview_kit_as_markdown(kit_data)
        return self.export_to_markdown(md_content, "Interview_Preparation_Kit")

    def _format_resume_as_markdown(self, resume_data: dict[str, Any]) -> str:
        """Format resume data as Markdown.

        Args:
            resume_data: Resume data

        Returns:
            Markdown formatted resume
        """
        lines = []

        # Header
        if resume_data.get("name"):
            lines.append(f"# {resume_data['name']}")
        if resume_data.get("email") or resume_data.get("phone"):
            lines.append(f"{resume_data.get('email', '')} | {resume_data.get('phone', '')}")
        lines.append("")

        # Summary
        if resume_data.get("summary"):
            lines.append("## Summary")
            lines.append(resume_data["summary"])
            lines.append("")

        # Experience
        if resume_data.get("experience"):
            lines.append("## Experience")
            for exp in resume_data["experience"]:
                lines.append(f"### {exp.get('title', '')} at {exp.get('company', '')}")
                if exp.get("dates"):
                    lines.append(f"*{exp['dates']}*")
                if exp.get("description"):
                    lines.append(exp["description"])
                if exp.get("achievements"):
                    for achievement in exp["achievements"]:
                        lines.append(f"- {achievement}")
                lines.append("")

        # Education
        if resume_data.get("education"):
            lines.append("## Education")
            for edu in resume_data["education"]:
                lines.append(f"### {edu.get('degree', '')} - {edu.get('institution', '')}")
                if edu.get("year"):
                    lines.append(f"*{edu['year']}*")
                lines.append("")

        # Skills
        if resume_data.get("skills"):
            lines.append("## Skills")
            for category, skills in resume_data["skills"].items():
                lines.append(f"**{category.title()}:** {', '.join(skills)}")
            lines.append("")

        # Projects
        if resume_data.get("projects"):
            lines.append("## Projects")
            for project in resume_data["projects"]:
                lines.append(f"### {project.get('name', '')}")
                if project.get("description"):
                    lines.append(project["description"])
                if project.get("technologies"):
                    lines.append(f"**Technologies:** {', '.join(project['technologies'])}")
                lines.append("")

        return "\n".join(lines)

    def _format_interview_kit_as_markdown(self, kit_data: dict[str, Any]) -> str:
        """Format interview kit as Markdown.

        Args:
            kit_data: Interview kit data

        Returns:
            Markdown formatted interview kit
        """
        lines = []

        # Header
        company = kit_data.get("company_name", "Company")
        role = kit_data.get("role_title", "Role")
        lines.append(f"# Interview Preparation Kit")
        lines.append(f"**Company:** {company}")
        lines.append(f"**Role:** {role}")
        lines.append("")

        # Company Overview
        if kit_data.get("company_overview"):
            lines.append("## Company Overview")
            lines.append(kit_data["company_overview"])
            lines.append("")

        # Role Overview
        if kit_data.get("role_overview"):
            lines.append("## Role Overview")
            lines.append(kit_data["role_overview"])
            lines.append("")

        # Responsibilities
        if kit_data.get("responsibilities"):
            lines.append("## Key Responsibilities")
            for resp in kit_data["responsibilities"]:
                lines.append(f"- {resp}")
            lines.append("")

        # Technical Topics
        if kit_data.get("technical_topics"):
            lines.append("## Technical Topics")
            for topic in kit_data["technical_topics"]:
                lines.append(f"### {topic['topic']} (Priority: {topic['priority']})")
                if topic.get("resources"):
                    lines.append("**Resources:**")
                    for resource in topic["resources"]:
                        lines.append(f"- {resource}")
                lines.append("")

        # Behavioral Questions
        if kit_data.get("behavioral_questions"):
            lines.append("## Behavioral Questions")
            for q in kit_data["behavioral_questions"]:
                lines.append(f"### {q['question']} (Priority: {q['priority']})")
                lines.append(f"**STAR Suggestion:** {q['star_suggestion']}")
                lines.append("")

        # Project Questions
        if kit_data.get("project_questions"):
            lines.append("## Project Discussion Questions")
            for q in kit_data["project_questions"]:
                lines.append(f"### {q['question']} (Priority: {q['priority']})")
                lines.append(f"**Suggested Answer:** {q['suggested_answer']}")
                lines.append("")

        # Questions to Ask
        if kit_data.get("questions_to_ask"):
            lines.append("## Questions to Ask the Interviewer")
            for q in kit_data["questions_to_ask"]:
                lines.append(f"- {q['question']}")
                lines.append(f"  *Reason: {q['reason']}*")
            lines.append("")

        # Study Plans
        if kit_data.get("study_plan_90min"):
            lines.append("## 90-Minute Study Plan")
            for item in kit_data["study_plan_90min"]:
                lines.append(f"- **{item['time']}**: {item['task']} (Priority: {item['priority']})")
            lines.append("")

        return "\n".join(lines)


# Global instance
export_engine = ExportEngine()
