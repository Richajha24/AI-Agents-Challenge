from typing import Any

from app.agents.base import BaseResearchAgent
from app.schemas.competitor import CompetitorIntelligenceOutput


class CompetitorIntelligenceAgent(BaseResearchAgent):
    analysis_type = "competitor"

    @property
    def output_schema(self) -> dict[str, Any]:
        return CompetitorIntelligenceOutput.model_json_schema()

    def build_prompt(self, data: dict[str, Any]) -> str:
        competitors = ", ".join(data["competitor_names"])
        return f"""You are a competitive-intelligence analyst.
Industry: {data['industry']}
Competitors: {competitors}
For each competitor, assess positioning, strengths, and weaknesses. Then synthesize the
competitive landscape and differentiation insights. Qualify uncertain claims and do not
invent facts or funding data. Return only JSON matching the requested schema."""

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.provider.generate_structured(self.build_prompt(input_data), self.output_schema)
        return CompetitorIntelligenceOutput.model_validate(result).model_dump()
