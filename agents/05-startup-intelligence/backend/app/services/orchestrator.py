from typing import Any

from sqlalchemy.orm import Session

from app.models.research_analysis import ResearchAnalysis
from app.agents.competitor_intelligence import CompetitorIntelligenceAgent
from app.agents.market_intelligence import MarketIntelligenceAgent
from app.agents.swot_analysis import SWOTAnalysisAgent
from app.agents.trend_discovery import TrendDiscoveryAgent
from app.core.config import get_settings
from app.providers.factory import get_provider
from app.services.progress_tracker import ProgressTracker
from app.services.report_generator import ReportGenerator


class ResearchOrchestrator:
    """Runs approved research agents and persists their reports."""

    def __init__(self, db: Session):
        self.db = db
        self.progress = ProgressTracker()
        self.reports = ReportGenerator()

    def start_analysis(
        self, *, user_id: str, analysis_type: str, input_data: dict[str, Any]
    ) -> ResearchAnalysis:
        analysis = ResearchAnalysis(
            user_id=user_id,
            analysis_type=analysis_type,
            input_data=input_data,
            status="pending",
            progress=0,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    async def execute_analysis(self, analysis: ResearchAnalysis):
        try:
            self.progress.update(analysis, status="processing", progress=10)
            self.db.commit()
            agent_class = {"market": MarketIntelligenceAgent, "competitor": CompetitorIntelligenceAgent,
                           "trend": TrendDiscoveryAgent, "swot": SWOTAnalysisAgent}[analysis.analysis_type]
            agent = agent_class(get_provider(get_settings().ai_provider))
            analysis.results = await agent.run(analysis.input_data)
            self.progress.update(analysis, status="processing", progress=85)
            self.db.commit()
            report = self.reports.create(self.db, analysis)
            self.progress.update(analysis, status="completed", progress=100)
            self.db.commit()
            self.db.refresh(analysis)
            self.db.refresh(report)
            return analysis, report
        except Exception as exc:
            analysis.error_message = str(exc)
            self.progress.update(analysis, status="failed", progress=analysis.progress)
            self.db.commit()
            raise

    async def run_analysis(self, *, user_id: str, analysis_type: str, input_data: dict[str, Any]):
        analysis = self.start_analysis(user_id=user_id, analysis_type=analysis_type, input_data=input_data)
        return await self.execute_analysis(analysis)
