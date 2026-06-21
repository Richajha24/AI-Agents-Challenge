from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Analysis
from app.schemas import LinkedInAnalysisInput, AnalysisResult, AnalysisStatusResponse
from app.orchestrator import AnalysisOrchestrator
import logging
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

def run_analysis(orchestrator, analysis_id, profile_url, profile_info, industry, career_goals, target_audience):
    """Run analysis in a new event loop (for background thread)"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from app.database import AsyncSessionLocal
    async def _run():
        async with AsyncSessionLocal() as db:
            await orchestrator.execute_analysis(
                db=db,
                analysis_id=analysis_id,
                profile_url=profile_url,
                profile_info=profile_info,
                industry=industry,
                career_goals=career_goals,
                target_audience=target_audience
            )
    try:
        loop.run_until_complete(_run())
    except Exception as e:
        logger.error(f"Background task failed: {str(e)}", exc_info=True)
    finally:
        loop.close()

@router.post("/api/v1/profile/analyze", response_model=dict)
async def create_analysis(
    request: LinkedInAnalysisInput,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Create a new LinkedIn profile growth analysis"""
    try:
        analysis = Analysis(
            profile_url=request.profile_url,
            profile_info=request.profile_info,
            industry=request.industry,
            career_goals=request.career_goals,
            target_audience=request.target_audience,
            status="pending"
        )
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)

        orchestrator = AnalysisOrchestrator()
        background_tasks.add_task(
            run_analysis,
            orchestrator,
            analysis.id,
            request.profile_url,
            request.profile_info,
            request.industry,
            request.career_goals,
            request.target_audience
        )

        return {
            "analysis_id": str(analysis.id),
            "status": "pending",
            "message": "Analysis started. Check status for updates."
        }
    except Exception as e:
        logger.error(f"Error creating analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    analysis_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get analysis status and progress"""
    try:
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()

        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return AnalysisStatusResponse(
            analysis_id=analysis.id,
            status=analysis.status,
            progress=analysis.progress,
            created_at=analysis.created_at,
            updated_at=analysis.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/report/{analysis_id}", response_model=AnalysisResult)
async def get_report(
    analysis_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get complete analysis report"""
    try:
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await db.execute(stmt)
        analysis = result.scalar_one_or_none()

        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")

        if analysis.status != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Analysis not completed. Current status: {analysis.status}"
            )

        return AnalysisResult(
            analysis_id=analysis.id,
            status=analysis.status,
            progress=analysis.progress,
            profile_url=analysis.profile_url,
            industry=analysis.industry,
            career_goals=analysis.career_goals,
            target_audience=analysis.target_audience,
            profile_score=analysis.profile_score,
            profile_optimization=analysis.profile_optimization,
            personal_brand=analysis.personal_brand,
            content_strategy=analysis.content_strategy,
            post_generation=analysis.post_generation,
            growth_roadmap=analysis.growth_roadmap,
            created_at=analysis.created_at,
            completed_at=analysis.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/history", response_model=list)
async def get_analysis_history(
    db: AsyncSession = Depends(get_db),
    limit: int = 20
):
    """Get user's analysis history"""
    try:
        stmt = select(Analysis).order_by(Analysis.created_at.desc()).limit(limit)
        result = await db.execute(stmt)
        analyses = result.scalars().all()

        return [
            {
                "analysis_id": str(a.id),
                "profile_url": a.profile_url,
                "industry": a.industry,
                "status": a.status,
                "created_at": a.created_at,
                "completed_at": a.completed_at
            }
            for a in analyses
        ]
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
