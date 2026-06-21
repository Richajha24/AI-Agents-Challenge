import asyncio
import sys
sys.path.insert(0, '.')

from app.config import settings
from app.ai.provider import get_provider
from app.agents.profile_optimization import ProfileOptimizationAgent

provider = get_provider('gemini', settings.GOOGLE_API_KEY)
agent = ProfileOptimizationAgent(provider)

async def test():
    result = await agent.execute(
        profile_url='https://linkedin.com/in/test-user',
        profile_info='Senior Developer with 5 years experience in Python and cloud services.',
        industry='Software Development',
        career_goals='Find senior architect opportunities'
    )
    print(result)

asyncio.run(test())
