from typing import Any

from app.agents.base import BaseResearchAgent
from app.schemas.swot import SWOTAnalysisOutput


class SWOTAnalysisAgent(BaseResearchAgent):
    analysis_type = "swot"

    @property
    def output_schema(self) -> dict[str, Any]:
        return SWOTAnalysisOutput.model_json_schema()

    def build_prompt(self, data: dict[str, Any]) -> str:
        return f"""You are a startup strategy analyst.
Startup concept: {data['startup_concept']}
Produce a practical SWOT analysis. Separate internal strengths and weaknesses from
external opportunities and threats, then give strategic implications. Use only reasonable
inferences from the concept and do not fabricate facts. Return only JSON matching the
requested schema."""

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        result = await self.provider.generate_structured(self.build_prompt(input_data), self.output_schema)
        return SWOTAnalysisOutput.model_validate(result).model_dump()
