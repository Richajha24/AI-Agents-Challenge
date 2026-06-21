from typing import Dict, Any, List
from app.agents.base import Agent

class MeetingPreparationAgent(Agent):
    """Generates meeting briefs, agendas, discussion points, and risk areas."""
    
    async def execute(self, topic: str, participants: str = None, context: str = None, **kwargs) -> Dict[str, Any]:
        prompt = f"""
You are a world-class Executive Assistant. Your goal is to prepare the user thoroughly for their upcoming meeting.

Meeting Topic: {topic}
Participants: {participants or "Not specified"}
Context / Notes / Goals: {context or "Not specified"}

Please prepare a comprehensive brief, agenda, key discussion points, and potential risk areas for this meeting.

Respond ONLY with a JSON object containing the following keys (no markdown formatting, no backticks, no text before or after the JSON):
1. "brief": A short, clear overview/summary (2-4 sentences) explaining the main objective and importance of the meeting.
2. "agenda": A list of proposed agenda topics with recommended time allocations (e.g. "1. Welcome and setup (5 mins)").
3. "discussion_points": A list of critical questions, key points to raise, or suggestions for steering the conversation productively.
4. "risk_areas": A list of risks, warnings, sensitive issues, or caveats to watch out for during the meeting.

Format the JSON response cleanly.
"""
        
        # Define JSON schema for structured validation
        schema = {
            "type": "object",
            "properties": {
                "brief": {"type": "string"},
                "agenda": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "discussion_points": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "risk_areas": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["brief", "agenda", "discussion_points", "risk_areas"]
        }
        
        result = await self.provider.generate_json(prompt, schema)
        return result
