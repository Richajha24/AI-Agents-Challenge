from typing import Any

from app.providers.base import AIProvider


class GeminiProvider(AIProvider):
    name = "gemini"

    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Gemini integration is not part of Phase 1.")
