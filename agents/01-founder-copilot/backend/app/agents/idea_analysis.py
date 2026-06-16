from typing import Dict, Any
from app.agents.base import Agent
import json

class IdeaAnalysisAgent(Agent):
    """Analyzes startup ideas for viability and market potential"""
    
    async def execute(self, startup_idea: str, industry: str, problem_statement: str, **kwargs) -> Dict[str, Any]:
        prompt = f"""
Analyze this startup idea for market potential and viability:

Idea: {startup_idea}
Industry: {industry}
Problem Statement: {problem_statement}

Please provide a structured JSON analysis with:
1. problem_summary: Brief summary of the problem
2. opportunity_assessment: Assessment of the opportunity
3. market_attractiveness_score: Score from 1-100
4. risk_assessment: Key risks identified
5. key_insights: List of 3-5 key insights

Return ONLY valid JSON, no other text.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
