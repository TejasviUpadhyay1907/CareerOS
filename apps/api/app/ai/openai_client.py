"""OpenAI client wrapper with OpenRouter support."""
from typing import Any, Dict, Optional

import openai
import httpx
from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import ValidationError

logger = get_logger(__name__)


class OpenAIClient:
    """Wrapper for OpenAI API client with OpenRouter support."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = settings.openai_api_key
        self.use_openrouter = settings.use_openrouter
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self._client: Optional[openai.AsyncOpenAI] = None
        self._httpx_client: Optional[httpx.AsyncClient] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize OpenAI client."""
        if not self.api_key or self.api_key == "":
            logger.warning("API key not configured, AI features disabled")
            self._initialized = False
            return

        try:
            if self.use_openrouter:
                # Use direct httpx for OpenRouter to avoid OpenAI lib issues
                self._httpx_client = httpx.AsyncClient(
                    base_url=self.openrouter_base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://careeros.ai",
                        "X-Title": "CareerOS",
                    },
                    timeout=60.0
                )
                logger.info(f"OpenRouter client initialized successfully with API key: {self.api_key[:15]}...")
            else:
                # Configure for direct OpenAI
                self._client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}")
            self._initialized = False
            raise

    async def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: str = "openai/gpt-4o-mini",  # Default to OpenRouter format
        **kwargs: Any,
    ) -> str:
        """Generate chat completion."""
        if not self._initialized:
            raise ValidationError(
                "AI features are currently unavailable. Please configure API key to enable AI features."
            )

        try:
            if self.use_openrouter and self._httpx_client:
                # Use direct HTTP request for OpenRouter
                logger.info(f"Making OpenRouter request with model: {model}")
                
                payload = {
                    "model": model,
                    "messages": messages,
                    **kwargs
                }
                
                response = await self._httpx_client.post("/chat/completions", json=payload)
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                logger.info("OpenRouter completion successful")
                return content or ""
                
            elif self._client:
                # Use OpenAI client for direct OpenAI
                logger.info(f"Making OpenAI request with model: {model}")
                
                response = await self._client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **kwargs,
                )
                logger.info("OpenAI completion successful")
                return response.choices[0].message.content or ""
            else:
                raise ValidationError("No AI client available")
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            if hasattr(e, 'response') and e.response:
                error_detail = e.response.text
                logger.error(f"Error response: {error_detail}")
            raise ValidationError(f"AI service error: {str(e)}")
        except openai.APIError as e:
            logger.error(f"AI API error: {e}")
            raise ValidationError(f"AI service error: {str(e)}")
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise ValidationError(f"Failed to generate AI response: {str(e)}")

    async def close(self) -> None:
        """Close AI client connection."""
        if self._client:
            await self._client.close()
        if self._httpx_client:
            await self._httpx_client.aclose()
        provider = "OpenRouter" if self.use_openrouter else "OpenAI"
        logger.info(f"{provider} client connection closed")


# Global instance
openai_client = OpenAIClient()
