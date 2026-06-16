from typing import Dict, Any
from app.agents.base import Agent

class CustomerPersonaAgent(Agent):
    """Generate customer personas"""
    
    async def execute(self, startup_idea: str, industry: str, problem_statement: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Generate customer personas for this startup:

Idea: {startup_idea}
Industry: {industry}
Problem: {problem_statement}

Create a JSON response with:
1. personas: Array of 2-3 detailed personas with name, role, demographics, goals
2. primary_pain_points: List of 4-5 main pain points these customers face
3. buying_motivations: List of 4-5 reasons they would buy your product
4. behavioral_patterns: List of 3-4 key behavioral patterns

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
