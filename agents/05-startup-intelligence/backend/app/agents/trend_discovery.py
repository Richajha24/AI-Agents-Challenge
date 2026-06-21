from typing import Any

from app.agents.base import BaseResearchAgent
from app.schemas.trends import TrendDiscoveryOutput


class TrendDiscoveryAgent(BaseResearchAgent):
    analysis_type = "trend"

    @property
    def output_schema(self) -> dict[str, Any]:
        return TrendDiscoveryOutput.model_json_schema()

    def build_prompt(self, data: dict[str, Any]) -> str:
        return f"""You are a trend research analyst.
Industry: {data['industry']}
Identify material emerging trends. Distinguish early signals from established movements.
Describe technology shifts, growth sectors, and watch signals for a startup or investor.
Do not claim real-time verification or invent statistics. Return only JSON matching the
requested schema."""

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.provider.generate_structured(self.build_prompt(input_data), self.output_schema)
        return TrendDiscoveryOutput.model_validate(result).model_dump()
