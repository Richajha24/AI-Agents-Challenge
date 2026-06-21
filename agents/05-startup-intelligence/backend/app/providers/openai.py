from typing import Any

from app.providers.base import AIProvider


class OpenAIProvider(AIProvider):
    name = "openai"

    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("OpenAI integration is not part of Phase 1.")
