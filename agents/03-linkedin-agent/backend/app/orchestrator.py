from typing import Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Analysis
from app.ai.provider import get_provider
from app.agents.profile_optimization import ProfileOptimizationAgent
from app.agents.personal_brand import PersonalBrandAgent
from app.agents.content_strategy import ContentStrategyAgent
from app.agents.post_generation import PostGenerationAgent
from app.agents.growth_roadmap import GrowthRoadmapAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AnalysisOrchestrator:
    """Orchestrates all LinkedIn growth analysis agents"""
    
    def __init__(self):
        provider_key_map = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
        }
        provider_name = settings.DEFAULT_PROVIDER.lower()
        self.api_key = getattr(settings, provider_key_map.get(provider_name, ""), None)
        if not self.api_key:
            raise ValueError(f"API key not configured for provider: {settings.DEFAULT_PROVIDER}")
        self.provider = get_provider(provider_name, self.api_key)
        
    async def execute_analysis(
        self, 
        db: AsyncSession, 
        analysis_id: str,
        profile_url: str,
        profile_info: str,
        industry: str,
        career_goals: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Execute full LinkedIn profile and growth analysis"""
        
        try:
            # Get analysis record
            stmt = select(Analysis).where(Analysis.id == analysis_id)
            result = await db.execute(stmt)
            analysis = result.scalar_one()
            
            # Update status
            analysis.status = "in_progress"
            analysis.progress = 0
            await db.commit()
            
            agents_results = {}
            
            # 1. Profile Optimization (0-20%)
            logger.info(f"Running Profile Optimization for {analysis_id}")
            agent_opt = ProfileOptimizationAgent(self.provider)
            agents_results['profile_optimization'] = await agent_opt.execute(
                profile_url=profile_url,
                profile_info=profile_info,
                industry=industry,
                career_goals=career_goals
            )
            analysis.profile_optimization = agents_results['profile_optimization']
            analysis.profile_score = agents_results['profile_optimization'].get('score', 70)
            analysis.progress = 20
            await db.commit()
            
            # 2. Personal Brand (20-40%)
            logger.info(f"Running Personal Brand Strategy for {analysis_id}")
            agent_brand = PersonalBrandAgent(self.provider)
            agents_results['personal_brand'] = await agent_brand.execute(
                industry=industry,
                career_goals=career_goals,
                target_audience=target_audience,
                profile_optimization=agents_results['profile_optimization']
            )
            analysis.personal_brand = agents_results['personal_brand']
            analysis.progress = 40
            await db.commit()
            
            # 3. Content Strategy (40-60%)
            logger.info(f"Running Content Strategy for {analysis_id}")
            agent_strategy = ContentStrategyAgent(self.provider)
            agents_results['content_strategy'] = await agent_strategy.execute(
                personal_brand=agents_results['personal_brand'],
                industry=industry,
                career_goals=career_goals
            )
            analysis.content_strategy = agents_results['content_strategy']
            analysis.progress = 60
            await db.commit()
            
            # 4. Post Generation (60-80%)
            logger.info(f"Running Post Generation for {analysis_id}")
            agent_posts = PostGenerationAgent(self.provider)
            agents_results['post_generation'] = await agent_posts.execute(
                content_strategy=agents_results['content_strategy'],
                personal_brand=agents_results['personal_brand'],
                career_goals=career_goals
            )
            analysis.post_generation = agents_results['post_generation']
            analysis.progress = 80
            await db.commit()
            
            # 5. Growth Roadmap (80-100%)
            logger.info(f"Running Growth Roadmap for {analysis_id}")
            agent_roadmap = GrowthRoadmapAgent(self.provider)
            agents_results['growth_roadmap'] = await agent_roadmap.execute(
                personal_brand=agents_results['personal_brand'],
                career_goals=career_goals,
                profile_optimization=agents_results['profile_optimization']
            )
            analysis.growth_roadmap = agents_results['growth_roadmap']
            analysis.progress = 100
            analysis.status = "completed"
            analysis.completed_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"LinkedIn analysis completed successfully for {analysis_id}")
            return {
                "status": "completed",
                "analysis_id": str(analysis_id),
                "results": agents_results
            }
            
        except Exception as e:
            logger.error(f"Error during LinkedIn analysis {analysis_id}: {str(e)}")
            analysis.status = "failed"
            analysis.error_message = str(e)
            await db.commit()
            raise
