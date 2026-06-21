from sqlalchemy import text

from fastapi import APIRouter

from app.core.database import engine
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return HealthResponse(status="ok", database="ok")
