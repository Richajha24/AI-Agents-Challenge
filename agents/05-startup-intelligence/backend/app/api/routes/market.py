from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.routes._analysis import queue_analysis
from app.core.database import get_db
from app.schemas.common import AnalysisAccepted
from app.schemas.market import MarketAnalysisRequest

router = APIRouter(prefix="/market", tags=["market"])


@router.post("/analyze", response_model=AnalysisAccepted, status_code=status.HTTP_201_CREATED)
async def analyze_market(payload: MarketAnalysisRequest, db: Session = Depends(get_db)) -> AnalysisAccepted:
    return await queue_analysis(db=db, user_id=payload.user_id, analysis_type="market", input_data=payload.model_dump())
