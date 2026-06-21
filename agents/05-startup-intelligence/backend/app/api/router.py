from fastapi import APIRouter

from app.api.routes import competitor, health, market, reports, swot, trends

api_router = APIRouter(prefix="/api")
api_router.include_router(market.router)
api_router.include_router(competitor.router)
api_router.include_router(trends.router)
api_router.include_router(swot.router)
api_router.include_router(reports.router)
api_router.include_router(health.router)
