from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.report import Report
from app.schemas.common import ReportResponse

router = APIRouter(prefix="/report", tags=["reports"])


@router.get("/{id}", response_model=ReportResponse)
def get_report(id: str, db: Session = Depends(get_db)) -> Report:
    report = db.get(Report, id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
