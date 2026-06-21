from app.models.research_analysis import ResearchAnalysis


class ProgressTracker:
    def update(self, analysis: ResearchAnalysis, *, status: str, progress: int) -> None:
        analysis.status = status
        analysis.progress = max(0, min(100, progress))
