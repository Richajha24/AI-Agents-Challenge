from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AnalysisAccepted(BaseModel):
    id: str
    analysis_type: str
    status: str
    progress: int = Field(ge=0, le=100)
    results: dict[str, Any] | None = None
    report_id: str | None = None
    error_message: str | None = None


class ReportResponse(BaseModel):
    id: str
    analysis_id: str
    report_type: str
    content: dict[str, Any]
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    database: str
