from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import AnalysisAccepted
from app.services.orchestrator import ResearchOrchestrator


async def queue_analysis(*, db: Session, user_id: str, analysis_type: str, input_data: dict) -> AnalysisAccepted:
    analysis, report = await ResearchOrchestrator(db).run_analysis(
        user_id=user_id, analysis_type=analysis_type, input_data=input_data)
    return AnalysisAccepted(
        id=analysis.id,
        analysis_type=analysis.analysis_type,
        status=analysis.status,
        progress=analysis.progress,
        results=analysis.results,
        report_id=report.id,
    )
