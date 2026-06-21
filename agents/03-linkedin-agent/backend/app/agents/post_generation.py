from typing import Dict, Any
from app.agents.base import Agent

class PostGenerationAgent(Agent):
    """Generates ready-to-publish LinkedIn posts, stories, and engaging hooks"""
    
    async def execute(
        self, 
        content_strategy: Dict[str, Any], 
        personal_brand: Dict[str, Any], 
        career_goals: str, 
        **kwargs
    ) -> Dict[str, Any]:
        prompt = f"""
You are an expert copywriter specializing in LinkedIn content. Write 3 highly engaging, professional posts.

Brand Identity & Positioning: {personal_brand}
Content Strategy & Calendar Concepts: {content_strategy}
Career Goals: {career_goals}

For each post, design it to feel authentic and conversational, using proper whitespace, spacing, and a strong hook. Do not use overly promotional language, corporate jargon, or generic templates. 

Generate a structured JSON response with:
1. posts: A list of 3 post objects. Each object must contain:
   - post_id: Integer (1, 2, 3)
   - theme: The theme of the post (e.g. "Educational", "Personal Story", "Industry Opinion")
   - hook: The single high-impact opening line
   - body: The body of the post. Use line breaks to separate ideas and keep paragraphs short (1-2 sentences).
   - hashtags: A list of 2-3 relevant hashtags
2. hooks: A list of 5 alternative general hooks that the user can use for writing other posts in the future.

Return ONLY valid JSON matching this structure, no other text, no markdown backticks.
"""
        result = await self.provider.generate_json(prompt, {})
        return result
