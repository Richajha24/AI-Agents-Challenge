from typing import Dict, Any
from app.agents.base import Agent

class GrowthRoadmapAgent(Agent):
    """Generates actionable 30, 60, and 90 day growth plans and milestones"""
    
    async def execute(
        self, 
        personal_brand: Dict[str, Any], 
        career_goals: str, 
        profile_optimization: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        prompt = f"""
You are a strategic career growth advisor. Create a clear roadmap to help the user build their LinkedIn presence and hit their career goals.

Brand Identity & Positioning: {personal_brand}
Profile Optimization Feedback: {profile_optimization}
Career Goals: {career_goals}

Generate a structured JSON response with:
1. thirty_day_plan: A list of 3-5 specific actions/tasks to complete in the first 30 days (e.g. updating profile, launching the first few posts).
2. sixty_day_plan: A list of 3-5 specific actions/tasks to complete in days 31-60 (e.g. daily comment engagements, networking with specific roles).
3. ninety_day_plan: A list of 3-5 specific actions/tasks to complete in days 61-90 (e.g. starting a newsletter, asking for recommendations, reaching out to target prospects).
4. milestones: A list of 3 growth milestones or KPIs to measure success (e.g., connection targets, engagement metrics, profile views).

Return ONLY valid JSON matching this structure, no other text, no markdown backticks.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
