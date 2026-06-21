from typing import Any

from app.providers.base import AIProvider


class ClaudeProvider(AIProvider):
    name = "claude"

    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Claude integration is not part of Phase 1.")
