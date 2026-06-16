from typing import Dict, Any
from app.agents.base import Agent

class CompetitorResearchAgent(Agent):
    """Research and analyze competitors"""
    
    async def execute(self, startup_idea: str, industry: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Research competitors for this startup idea:

Idea: {startup_idea}
Industry: {industry}

Please provide a JSON analysis with:
1. direct_competitors: List of 3-5 direct competitors with name, features, pricing
2. indirect_competitors: List of 2-3 indirect competitors
3. comparison_table: Comparison of key features across competitors
4. differentiation_opportunities: List of ways to differentiate

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
