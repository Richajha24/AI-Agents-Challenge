from typing import Dict, Any
from app.agents.base import Agent

class ContentStrategyAgent(Agent):
    """Generates weekly content calendars, monthly strategies, themes, and viral opportunities"""
    
    async def execute(
        self, 
        personal_brand: Dict[str, Any], 
        industry: str, 
        career_goals: str, 
        **kwargs
    ) -> Dict[str, Any]:
        prompt = f"""
You are an expert social media strategist specializing in LinkedIn growth.

Brand Identity & Positioning: {personal_brand}
Industry: {industry}
Career Goals: {career_goals}

Develop a comprehensive content strategy and calendar. Generate a structured JSON response with:
1. weekly_calendar: A list of 5 calendar items (representing Monday through Friday). Each item must contain:
   - day: The day of the week
   - pillar: Which brand content pillar it aligns with
   - post_concept: A brief explanation/angle of what the post will cover
2. monthly_strategy: A high-level focus and action plan for the next 30 days to build audience engagement.
3. content_themes: A list of 3 overarching themes/angles to use (e.g. "Behind the scenes", "Tutorials", "Thought leadership").
4. viral_opportunities: Actionable ideas or formats (like carousels, industry hot-takes, templates) that could yield wider distribution.

Return ONLY valid JSON matching this structure, no other text, no markdown backticks.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
