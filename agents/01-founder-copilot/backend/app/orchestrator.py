from typing import Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Analysis
from app.ai.provider import get_provider
from app.agents.idea_analysis import IdeaAnalysisAgent
from app.agents.competitor_research import CompetitorResearchAgent
from app.agents.market_research import MarketResearchAgent
from app.agents.customer_personas import CustomerPersonaAgent
from app.agents.mvp_planner import MVPPlannerAgent
from app.agents.pricing_strategy import PricingStrategyAgent
from app.agents.go_to_market import GoToMarketAgent
from app.agents.execution_roadmap import ExecutionRoadmapAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AnalysisOrchestrator:
    """Orchestrates all analysis agents"""
    
    def __init__(self):
        self.api_key = getattr(settings, f"{settings.DEFAULT_PROVIDER.upper()}_API_KEY", None)
        if not self.api_key:
            raise ValueError(f"API key not configured for provider: {settings.DEFAULT_PROVIDER}")
        self.provider = get_provider(settings.DEFAULT_PROVIDER, self.api_key)
    
    async def execute_analysis(
        self, 
        db: AsyncSession, 
        analysis_id: str,
        startup_idea: str,
        industry: str,
        problem_statement: str,
        website_url: str = None
    ) -> Dict[str, Any]:
        """Execute full startup analysis"""
        
        try:
            # Get analysis record
            stmt = select(Analysis).where(Analysis.id == analysis_id)
            result = await db.execute(stmt)
            analysis = result.scalar_one()
            
            # Update status
            analysis.status = "in_progress"
            analysis.progress = 0
            await db.commit()
            
            # Execute agents sequentially
            agents_results = {}
            
            # 1. Idea Analysis (0-12%)
            logger.info(f"Running Idea Analysis for {analysis_id}")
            agent = IdeaAnalysisAgent(self.provider)
            agents_results['idea_analysis'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry,
                problem_statement=problem_statement
            )
            analysis.idea_analysis = agents_results['idea_analysis']
            analysis.progress = 12
            await db.commit()
            
            # 2. Competitor Research (12-25%)
            logger.info(f"Running Competitor Research for {analysis_id}")
            agent = CompetitorResearchAgent(self.provider)
            agents_results['competitor_analysis'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.competitor_analysis = agents_results['competitor_analysis']
            analysis.progress = 25
            await db.commit()
            
            # 3. Market Research (25-37%)
            logger.info(f"Running Market Research for {analysis_id}")
            agent = MarketResearchAgent(self.provider)
            agents_results['market_research'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.market_research = agents_results['market_research']
            analysis.progress = 37
            await db.commit()
            
            # 4. Customer Personas (37-50%)
            logger.info(f"Running Customer Persona Analysis for {analysis_id}")
            agent = CustomerPersonaAgent(self.provider)
            agents_results['customer_personas'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry,
                problem_statement=problem_statement
            )
            analysis.customer_personas = agents_results['customer_personas']
            analysis.progress = 50
            await db.commit()
            
            # 5. MVP Planner (50-62%)
            logger.info(f"Running MVP Planning for {analysis_id}")
            agent = MVPPlannerAgent(self.provider)
            agents_results['mvp_plan'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.mvp_plan = agents_results['mvp_plan']
            analysis.progress = 62
            await db.commit()
            
            # 6. Pricing Strategy (62-75%)
            logger.info(f"Running Pricing Strategy for {analysis_id}")
            agent = PricingStrategyAgent(self.provider)
            agents_results['pricing_strategy'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.pricing_strategy = agents_results['pricing_strategy']
            analysis.progress = 75
            await db.commit()
            
            # 7. Go-To-Market (75-87%)
            logger.info(f"Running Go-To-Market Analysis for {analysis_id}")
            agent = GoToMarketAgent(self.provider)
            agents_results['go_to_market'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.go_to_market = agents_results['go_to_market']
            analysis.progress = 87
            await db.commit()
            
            # 8. Execution Roadmap (87-100%)
            logger.info(f"Running Execution Roadmap for {analysis_id}")
            agent = ExecutionRoadmapAgent(self.provider)
            agents_results['execution_roadmap'] = await agent.execute(
                startup_idea=startup_idea,
                industry=industry
            )
            analysis.execution_roadmap = agents_results['execution_roadmap']
            analysis.progress = 100
            analysis.status = "completed"
            analysis.completed_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"Analysis completed for {analysis_id}")
            return {
                "status": "completed",
                "analysis_id": str(analysis_id),
                "results": agents_results
            }
            
        except Exception as e:
            logger.error(f"Error during analysis {analysis_id}: {str(e)}")
            analysis.status = "failed"
            analysis.error_message = str(e)
            await db.commit()
            raise
