"""Reusable Groq API client for patent analysis."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError

load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqClientError(Exception):
    """Base error for Groq client operations."""


class GroqConfigurationError(GroqClientError):
    """Raised when required configuration is missing."""


class GroqClient:
    """Thin wrapper around the Groq SDK for chat completions."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise GroqConfigurationError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        self.model = model or os.getenv("MODEL_NAME") or os.getenv("GROQ_MODEL") or DEFAULT_MODEL
        self._client = Groq(api_key=self.api_key)

    @staticmethod
    def load_system_prompt(prompt_path: Path | None = None) -> str:
        path = prompt_path or Path(__file__).parent / "prompts" / "system_prompt.md"
        if not path.exists():
            raise GroqClientError(f"System prompt not found: {path}")
        return path.read_text(encoding="utf-8")

    def analyze_patent(self, patent_context: str, system_prompt: str | None = None) -> str:
        """Send patent context to Groq and return the structured analysis."""
        prompt = system_prompt or self.load_system_prompt()
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": patent_context},
        ]
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=4096,
            )
        except RateLimitError as exc:
            raise GroqClientError("Groq rate limit reached. Wait and try again.") from exc
        except APIConnectionError as exc:
            raise GroqClientError("Could not connect to Groq API. Check your network.") from exc
        except APIStatusError as exc:
            raise GroqClientError(
                f"Groq API error: {getattr(exc, 'message', None) or str(exc)}"
            ) from exc

        content = response.choices[0].message.content
        if not content:
            raise GroqClientError("Groq returned an empty response.")
        return content.strip()

