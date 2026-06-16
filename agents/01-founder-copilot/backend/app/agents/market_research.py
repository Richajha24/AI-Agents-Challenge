from typing import Dict, Any
from app.agents.base import Agent

class MarketResearchAgent(Agent):
    """Perform market research and sizing"""
    
    async def execute(self, startup_idea: str, industry: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Perform market research for this startup:

Idea: {startup_idea}
Industry: {industry}

Estimate and provide a JSON analysis with:
1. tam: Total Addressable Market size estimate
2. sam: Serviceable Available Market estimate
3. som: Serviceable Obtainable Market estimate
4. market_size_estimate: Overall market size estimation
5. industry_trends: List of 3-5 current industry trends
6. growth_opportunities: List of 3-5 growth opportunities

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
