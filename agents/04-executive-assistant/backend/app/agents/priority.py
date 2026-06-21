from typing import Dict, Any, List
from app.agents.base import Agent
import json

class PriorityManagementAgent(Agent):
    """Prioritizes tasks, recommends focus areas, and identifies the critical path."""
    
    async def execute(self, tasks: List[Dict[str, Any]], goals: str = None, **kwargs) -> Dict[str, Any]:
        if not tasks:
            return {
                "priority_ranking": [],
                "focus_recommendations": ["No tasks provided. Add tasks to start planning."],
                "critical_path": []
            }
            
        tasks_str = json.dumps(tasks, indent=2)
        
        prompt = f"""
You are a world-class Executive Assistant. Your goal is to analyze the user's tasks and prioritize them strategically.

Goals / Priorities for the period:
{goals or "Not specified"}

Tasks to prioritize:
{tasks_str}

Please analyze this input and rank the tasks by priority. Categorize them and provide strategic reasoning for the ranking, alignment with goals, and deadline urgency.

Respond ONLY with a JSON object containing the following keys (no markdown formatting, no backticks, no text before or after the JSON):
1. "priority_ranking": A list of prioritized tasks. Each item MUST have:
   - "title": Title of the task.
   - "priority": "high", "medium", or "low".
   - "category": Category of the task (e.g. Operations, Strategic, Urgent, Admin).
   - "reasoning": Rationale for this priority assignment.
2. "focus_recommendations": A list of 3-5 actionable recommendations/guidelines for the user on how to structure their focus (e.g. time blocking, deep work focus).
3. "critical_path": A list of task titles representing the critical path (the sequence of dependent or high-impact tasks that must be executed to unlock goals).

Format the JSON response cleanly.
"""
        
        # Define JSON schema for structured validation
        schema = {
            "type": "object",
            "properties": {
                "priority_ranking": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                            "category": {"type": "string"},
                            "reasoning": {"type": "string"}
                        },
                        "required": ["title", "priority", "category", "reasoning"]
                    }
                },
                "focus_recommendations": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "critical_path": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["priority_ranking", "focus_recommendations", "critical_path"]
        }
        
        result = await self.provider.generate_json(prompt, schema)
        return result
