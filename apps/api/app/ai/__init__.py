"""AI module for CareerOS."""
from app.ai.lemma_client import lemma_client
from app.ai.openai_client import openai_client

__all__ = ["lemma_client", "openai_client"]
