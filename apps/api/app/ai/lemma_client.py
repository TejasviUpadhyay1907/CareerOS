"""
Lemma SDK client for CareerOS.
Uses Lemma as a datastore and workflow layer for:
- Storing job applications in Lemma tables
- Storing resume files in Lemma file store
- Running career advice workflows through Lemma agents
"""
import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)


def _get_lemma_config():
    """Get Lemma config from settings."""
    try:
        from app.core.config import settings
        return settings.lemma_base_url, settings.lemma_api_key, settings.lemma_pod_id
    except Exception:
        return (
            os.environ.get("LEMMA_BASE_URL", "http://127-0-0-1.sslip.io:8711"),
            os.environ.get("LEMMA_API_KEY", ""),
            os.environ.get("LEMMA_POD_ID", ""),
        )


class LemmaClient:
    """
    Client for Lemma SDK integration.
    
    Lemma provides:
    - Tables: structured data store for job applications and resume analysis
    - Files: document store for resumes
    - Agents: AI agents with pod context
    - Workflows: multi-step automation pipelines
    """

    def __init__(self):
        self._client = None
        self._pod = None
        base_url, api_key, pod_id = _get_lemma_config()
        self._base_url = base_url
        self._api_key = api_key
        self._pod_id = pod_id
        self._enabled = bool(api_key and pod_id)

    def is_enabled(self) -> bool:
        return self._enabled

    async def initialize(self) -> bool:
        """Initialize Lemma SDK client."""
        if not self._enabled:
            logger.info("Lemma SDK not configured — skipping (set LEMMA_API_KEY and LEMMA_POD_ID)")
            return False
        try:
            from lemma_sdk import Lemma
            self._client = Lemma(
                base_url=self._base_url,
                api_key=self._api_key,
            )
            self._pod = self._client.pod(self._pod_id)
            logger.info(f"Lemma SDK initialized — pod={self._pod_id}")
            return True
        except Exception as e:
            logger.warning(f"Lemma SDK init failed: {e} — continuing without Lemma")
            self._enabled = False
            return False

    async def store_job_application(self, application_data: dict[str, Any]) -> Optional[str]:
        """
        Store a job application in Lemma table.
        This is the Lemma SDK's core 'tables + records' feature.
        """
        if not self._pod:
            return None
        try:
            table = self._pod.table("job_applications")
            record = table.records.create(data={
                "user_id":      application_data.get("user_id", ""),
                "company":      application_data.get("company", ""),
                "role":         application_data.get("role", ""),
                "status":       application_data.get("status", "applied"),
                "notes":        application_data.get("notes", ""),
                "applied_date": application_data.get("applied_date", ""),
                "job_url":      application_data.get("job_url", ""),
            })
            logger.info(f"Stored application in Lemma: {record.id}")
            return record.id
        except Exception as e:
            logger.warning(f"Lemma store_job_application failed: {e}")
            return None

    async def store_resume_analysis(self, resume_data: dict[str, Any]) -> Optional[str]:
        """
        Store resume analysis results in Lemma table.
        Uses Lemma's structured datastore.
        """
        if not self._pod:
            return None
        try:
            table = self._pod.table("resume_analyses")
            record = table.records.create(data={
                "user_id":      resume_data.get("user_id", ""),
                "filename":     resume_data.get("filename", ""),
                "health_score": resume_data.get("health_score", 0),
                "domain":       resume_data.get("domain", ""),
                "career_level": resume_data.get("career_level", ""),
                "strengths":    ", ".join(resume_data.get("strengths", [])),
                "skills":       ", ".join(resume_data.get("skills", [])),
                "years_exp":    resume_data.get("years_of_experience", 0),
            })
            logger.info(f"Stored resume analysis in Lemma: {record.id}")
            return record.id
        except Exception as e:
            logger.warning(f"Lemma store_resume_analysis failed: {e}")
            return None

    async def upload_resume_file(self, filename: str, content: bytes) -> Optional[str]:
        """
        Upload resume file to Lemma file store.
        Uses Lemma's document/file storage.
        """
        if not self._pod:
            return None
        try:
            file_obj = self._pod.files.upload(
                name=filename,
                content=content,
                content_type="application/pdf",
            )
            logger.info(f"Uploaded resume to Lemma files: {file_obj.id}")
            return file_obj.id
        except Exception as e:
            logger.warning(f"Lemma upload_resume_file failed: {e}")
            return None

    async def run_career_advice_workflow(self, user_context: str, question: str) -> Optional[str]:
        """
        Run career advice through a Lemma agent/workflow.
        Uses Lemma's agent infrastructure with pod context.
        """
        if not self._pod:
            return None
        try:
            # Use Lemma's agent conversation API
            conversation = self._pod.conversations.create(
                agent_slug="career-advisor",
                metadata={"source": "careeros"},
            )
            message = conversation.send(
                content=f"Context: {user_context}\n\nQuestion: {question}"
            )
            if message and message.content:
                logger.info("Got career advice from Lemma agent")
                return message.content
            return None
        except Exception as e:
            logger.warning(f"Lemma career workflow failed: {e}")
            return None


# Global singleton
lemma_client = LemmaClient()
