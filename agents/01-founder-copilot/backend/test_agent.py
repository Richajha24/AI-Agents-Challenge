import asyncio
import sys
sys.path.insert(0, '.')

from app.config import settings
from app.ai.provider import get_provider
from app.agents.idea_analysis import IdeaAnalysisAgent

provider = get_provider('gemini', settings.GOOGLE_API_KEY)
agent = IdeaAnalysisAgent(provider)

async def test():
    result = await agent.execute(
        startup_idea='An app for students to verify certificates',
        industry='EdTech',
        problem_statement='Fake certificates are common'
    )
    print(result)

asyncio.run(test())