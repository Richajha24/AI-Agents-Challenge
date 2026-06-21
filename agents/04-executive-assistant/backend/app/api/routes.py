from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
import asyncio
import logging

from app.database import get_db, AsyncSessionLocal
from app.models import Report, Decision
from app.schemas import (
    WorkspaceInput, ReportResult, ReportStatusResponse,
    TasksAnalyzeInput, MeetingPrepareInput, DecisionAnalyzeInput,
    PriorityAnalysisResult, MeetingPrepResult, DecisionSupportResult
)
from app.orchestrator import ExecutiveAssistantOrchestrator
from app.agents.priority import PriorityManagementAgent
from app.agents.meeting_prep import MeetingPreparationAgent
from app.agents.decision import DecisionSupportAgent

logger = logging.getLogger(__name__)
router = APIRouter()

# Background runner for workspace analysis
def run_workspace_analysis(orchestrator: ExecutiveAssistantOrchestrator, report_id: str, goals: str, tasks_input: List[Dict], meetings_input: List[Dict]):
    """Run full orchestration in a background thread/event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def _run():
        async with AsyncSessionLocal() as db:
            await orchestrator.execute_workspace_analysis(
                db=db,
                report_id=report_id,
                goals=goals,
                tasks_input=tasks_input,
                meetings_input=meetings_input
            )
            
    try:
        loop.run_until_complete(_run())
    except Exception as e:
        logger.error(f"Background workspace analysis task failed: {str(e)}", exc_info=True)
    finally:
        loop.close()

# 1. Workspace Analysis / Generate Report
@router.post("/api/report/generate", response_model=dict)
async def generate_report(
    request: WorkspaceInput,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Initiates a background daily planner workspace report analysis run"""
    try:
        # Create a new report record in DB
        report = Report(
            status="pending",
            goals=request.goals,
            tasks_input=[t.model_dump() for t in request.tasks_input],
            meetings_input=[m.model_dump() for m in request.meetings_input]
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        
        # Instantiate orchestrator and add background task
        orchestrator = ExecutiveAssistantOrchestrator()
        background_tasks.add_task(
            run_workspace_analysis,
            orchestrator,
            report.id,
            request.goals,
            report.tasks_input,
            report.meetings_input
        )
        
        return {
            "report_id": str(report.id),
            "status": "pending",
            "message": "Executive assistant analysis started in background."
        }
    except Exception as e:
        logger.error(f"Error generating workspace report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 2. Get Workspace Report Details
@router.get("/api/report/{id}", response_model=ReportResult)
async def get_report(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    """Fetches details, status, and outputs of a specific daily planner report"""
    try:
        stmt = select(Report).where(Report.id == id)
        res = await db.execute(stmt)
        report = res.scalar_one_or_none()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
            
        return ReportResult(
            report_id=report.id,
            status=report.status,
            progress=report.progress,
            goals=report.goals,
            tasks_input=report.tasks_input or [],
            meetings_input=report.meetings_input or [],
            priority_analysis=report.priority_analysis,
            meeting_briefs=report.meeting_briefs,
            daily_roadmap=report.daily_roadmap,
            created_at=report.created_at,
            completed_at=report.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving report {id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 3. Get Report History
@router.get("/api/report/history", response_model=List[Dict[str, Any]])
async def get_report_history(
    db: AsyncSession = Depends(get_db),
    limit: int = 20
):
    """Lists past workspaces and reports"""
    try:
        stmt = select(Report).order_by(Report.created_at.desc()).limit(limit)
        res = await db.execute(stmt)
        reports = res.scalars().all()
        
        return [
            {
                "report_id": r.id,
                "status": r.status,
                "progress": r.progress,
                "goals": r.goals,
                "created_at": r.created_at,
                "completed_at": r.completed_at
            }
            for r in reports
        ]
    except Exception as e:
        logger.error(f"Error fetching report history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 4. Individual Tasks Analyze Endpoint
@router.post("/api/tasks/analyze", response_model=PriorityAnalysisResult)
async def analyze_tasks(
    request: TasksAnalyzeInput
):
    """Runs priority analysis for a list of tasks synchronously"""
    try:
        orchestrator = ExecutiveAssistantOrchestrator()
        agent = PriorityManagementAgent(orchestrator.provider)
        result = await agent.execute(
            tasks=[t.model_dump() for t in request.tasks],
            goals=request.goals
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 5. Individual Meetings Prepare Endpoint
@router.post("/api/meetings/prepare", response_model=MeetingPrepResult)
async def prepare_meeting(
    request: MeetingPrepareInput
):
    """Prepares meeting agenda and brief synchronously"""
    try:
        orchestrator = ExecutiveAssistantOrchestrator()
        agent = MeetingPreparationAgent(orchestrator.provider)
        result = await agent.execute(
            topic=request.topic,
            participants=request.participants,
            context=request.context
        )
        return result
    except Exception as e:
        logger.error(f"Error preparing meeting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 6. Decision Support Endpoint
@router.post("/api/decisions/analyze", response_model=DecisionSupportResult)
async def analyze_decision(
    request: DecisionAnalyzeInput,
    db: AsyncSession = Depends(get_db)
):
    """Analyzes options for a decision dilemma and records result in DB"""
    try:
        orchestrator = ExecutiveAssistantOrchestrator()
        agent = DecisionSupportAgent(orchestrator.provider)
        analysis = await agent.execute(
            problem_statement=request.problem_statement,
            options=request.options
        )
        
        # Persist decision to DB
        decision = Decision(
            problem_statement=request.problem_statement,
            options=request.options,
            analysis_result=analysis
        )
        db.add(decision)
        await db.commit()
        
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing decision: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 7. Decision History Endpoint
@router.get("/api/decisions/history", response_model=List[Dict[str, Any]])
async def get_decision_history(
    db: AsyncSession = Depends(get_db),
    limit: int = 20
):
    """Lists past decision dilemmas and options"""
    try:
        stmt = select(Decision).order_by(Decision.created_at.desc()).limit(limit)
        res = await db.execute(stmt)
        decisions = res.scalars().all()
        
        return [
            {
                "decision_id": d.id,
                "problem_statement": d.problem_statement,
                "options": d.options,
                "analysis_result": d.analysis_result,
                "created_at": d.created_at
            }
            for d in decisions
        ]
    except Exception as e:
        logger.error(f"Error fetching decision history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 8. Calendar Optimize Endpoint (Phase 2 Stub)
@router.post("/api/calendar/optimize", response_model=dict)
async def optimize_calendar():
    """Stub endpoint for Calendar Optimization Agent (Phase 2)"""
    return {
        "status": "stub",
        "message": "Calendar Optimization Agent is scheduled for Phase 2."
    }

# 9. Follow-Up Generate Endpoint (Phase 2 Stub)
@router.post("/api/followup/generate", response_model=dict)
async def generate_followup():
    """Stub endpoint for Follow-Up Agent (Phase 2)"""
    return {
        "status": "stub",
        "message": "Follow-Up Agent is scheduled for Phase 2."
    }

# 10. Health Check
@router.get("/api/health", response_model=dict)
async def health_check():
    """Service health status"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
