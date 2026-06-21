import asyncio
import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, select

from app.core.database import SessionLocal, initialize_database
from app.models.report import Report
from app.models.research_analysis import ResearchAnalysis
from app.services.orchestrator import ResearchOrchestrator
import app.services.orchestrator as orchestrator_module
from app.api.routes.competitor import analyze_competitor
from app.api.routes.market import analyze_market
from app.api.routes.swot import analyze_swot
from app.api.routes.trends import discover_trends
from app.schemas.competitor import CompetitorAnalysisRequest
from app.schemas.market import MarketAnalysisRequest
from app.schemas.swot import SWOTAnalysisRequest
from app.schemas.trends import TrendDiscoveryRequest


class FakeProvider:
    name = "fake"

    async def generate_structured(self, prompt, schema):
        assert "Return only JSON" in prompt
        required = schema["required"]
        if "market_overview" in required:
            return {"market_overview": "Overview", "growth_indicators": ["Signal"], "opportunity_areas": ["Area"], "market_size_context": "Assumption", "key_assumptions": ["Assumption"]}
        if "competitor_analysis" in required:
            return {"competitor_analysis": [{"name": "Rival", "positioning": "Position", "strengths": ["S"], "weaknesses": ["W"]}], "competitive_landscape": "Landscape", "differentiation_insights": ["Insight"]}
        if "emerging_trends" in required:
            return {"emerging_trends": [{"trend": "AI", "description": "Growth", "maturity": "Emerging", "relevance": "High"}], "technology_shifts": ["Shift"], "growth_sectors": ["Sector"], "watch_signals": ["Signal"]}
        return {"strengths": ["S"], "weaknesses": ["W"], "opportunities": ["O"], "threats": ["T"], "strategic_implications": ["Act"]}


async def run():
    initialize_database()
    orchestrator_module.get_provider = lambda _: FakeProvider()
    cases = [("market", {"user_id": "user-1", "industry": "FinTech", "startup_idea": "Payments"}),
             ("competitor", {"user_id": "user-1", "industry": "FinTech", "competitor_names": ["Rival"]}),
             ("trend", {"user_id": "user-1", "industry": "FinTech"}),
             ("swot", {"user_id": "user-1", "startup_concept": "Payments"})]
    with SessionLocal() as db:
        for kind, data in cases:
            analysis, report = await ResearchOrchestrator(db).run_analysis(user_id=data["user_id"], analysis_type=kind, input_data=data)
            assert analysis.status == "completed" and analysis.progress == 100 and analysis.results
            assert report.analysis_id == analysis.id and report.content["findings"] == analysis.results
        assert db.scalar(select(func.count()).select_from(ResearchAnalysis)) == 4
        assert db.scalar(select(func.count()).select_from(Report)) == 4
    print("phase_2_agents_orchestration_persistence_reports=ok")


asyncio.run(run())

async def verify_route_handlers():
    orchestrator_module.get_provider = lambda _: FakeProvider()
    with SessionLocal() as db:
        responses = [
            await analyze_market(MarketAnalysisRequest(user_id="user-2", industry="FinTech", startup_idea="Payments"), db),
            await analyze_competitor(CompetitorAnalysisRequest(user_id="user-2", industry="FinTech", competitor_names=["Rival"]), db),
            await discover_trends(TrendDiscoveryRequest(user_id="user-2", industry="FinTech"), db),
            await analyze_swot(SWOTAnalysisRequest(user_id="user-2", startup_concept="Payments"), db),
        ]
        assert all(item.status == "completed" and item.report_id for item in responses)
asyncio.run(verify_route_handlers())
print("phase_2_endpoints=ok")
