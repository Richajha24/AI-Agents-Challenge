from typing import Dict, Any
from app.agents.base import Agent

class ExecutionRoadmapAgent(Agent):
    """Generate execution roadmap with timelines"""
    
    async def execute(self, startup_idea: str, industry: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Create an execution roadmap for this startup:

Idea: {startup_idea}
Industry: {industry}

Provide a JSON response with detailed plans for:
1. thirty_day_plan: Key objectives and milestones for 30 days
2. sixty_day_plan: Objectives and milestones for 60 days
3. ninety_day_plan: Objectives and milestones for 90 days
4. six_month_plan: Strategic objectives for 6 months
5. one_year_plan: Major goals and vision for 1 year

Each plan should include key initiatives, success metrics, and resource needs.

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
