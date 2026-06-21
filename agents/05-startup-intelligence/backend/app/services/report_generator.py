from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.research_analysis import ResearchAnalysis


class ReportGenerator:
    def create(self, db: Session, analysis: ResearchAnalysis) -> Report:
        report = Report(
            analysis_id=analysis.id,
            report_type=analysis.analysis_type,
            content={"analysis_type": analysis.analysis_type, "input": analysis.input_data,
                     "findings": analysis.results, "generated_at": datetime.now(timezone.utc).isoformat()},
        )
        db.add(report)
        return report
