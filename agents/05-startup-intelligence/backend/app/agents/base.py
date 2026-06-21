from abc import ABC, abstractmethod
from typing import Any

from app.providers.base import AIProvider


class BaseResearchAgent(ABC):
    analysis_type: str

    def __init__(self, provider: AIProvider):
        self.provider = provider

    @property
    @abstractmethod
    def output_schema(self) -> dict[str, Any]:
        """JSON Schema contract supplied to the AI provider."""

    @abstractmethod
    def build_prompt(self, input_data: dict[str, Any]) -> str:
        """Build an agent-specific, evidence-aware research prompt."""

    @property
    @abstractmethod
    def output_schema(self) -> dict[str, Any]:
        """JSON Schema contract supplied to the AI provider."""

    @abstractmethod
    def build_prompt(self, input_data: dict[str, Any]) -> str:
        """Build an agent-specific, evidence-aware research prompt."""

    @abstractmethod
    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute one research analysis; implementation is deferred beyond Phase 1."""
