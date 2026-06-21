from typing import Any

from app.agents.base import BaseResearchAgent
from app.schemas.market import MarketIntelligenceOutput


class MarketIntelligenceAgent(BaseResearchAgent):
    analysis_type = "market"

    @property
    def output_schema(self) -> dict[str, Any]:
        return MarketIntelligenceOutput.model_json_schema()

    def build_prompt(self, data: dict[str, Any]) -> str:
        return f"""You are a market intelligence analyst supporting a startup team.
Industry: {data['industry']}
Startup idea: {data['startup_idea']}
Provide a concise market overview, observable growth indicators, specific opportunity areas,
market-size context with labeled assumptions, and key assumptions. Do not invent statistics
or sources. Return only JSON matching the requested schema."""

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.provider.generate_structured(self.build_prompt(input_data), self.output_schema)
        return MarketIntelligenceOutput.model_validate(result).model_dump()
