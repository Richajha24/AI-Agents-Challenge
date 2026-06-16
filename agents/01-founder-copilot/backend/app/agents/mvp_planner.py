from typing import Dict, Any
from app.agents.base import Agent

class MVPPlannerAgent(Agent):
    """Generate MVP plan with prioritized features"""
    
    async def execute(self, startup_idea: str, industry: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Create an MVP plan for this startup:

Idea: {startup_idea}
Industry: {industry}

Provide a JSON response with:
1. core_features: List of 5-7 absolutely essential features
2. nice_to_have_features: List of 3-5 features to add later
3. development_priorities: Array with feature, complexity (easy/medium/hard), and estimated_days
4. estimated_timeline: Overall MVP timeline estimate (e.g., "8-10 weeks")

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
