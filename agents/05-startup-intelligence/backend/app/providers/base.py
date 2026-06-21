from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    name: str

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        """Return schema-conforming output. Provider integrations are deferred."""
