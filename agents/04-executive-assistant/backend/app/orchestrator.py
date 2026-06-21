from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Report
from app.ai.provider import get_provider
from app.agents.priority import PriorityManagementAgent
from app.agents.meeting_prep import MeetingPreparationAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ExecutiveAssistantOrchestrator:
    """Orchestrates implemented assistant agents for the daily workspace report"""
    
    def __init__(self):
        provider_key_map = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
        }
        self.api_key = getattr(settings, provider_key_map.get(settings.DEFAULT_PROVIDER.lower(), ""), None)
        if not self.api_key:
            raise ValueError(f"API key not configured for provider: {settings.DEFAULT_PROVIDER}")
        self.provider = get_provider(settings.DEFAULT_PROVIDER, self.api_key)
    
    async def execute_workspace_analysis(
        self,
        db: AsyncSession,
        report_id: str,
        goals: str = None,
        tasks_input: List[Dict[str, Any]] = None,
        meetings_input: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Runs the sequence of workspace agents in the background, updating progress."""
        try:
            # Retrieve report record
            stmt = select(Report).where(Report.id == report_id)
            result = await db.execute(stmt)
            report = result.scalar_one()
            
            # Start process
            report.status = "in_progress"
            report.progress = 5
            await db.commit()
            
            # 1. Priority Management Agent (5-50%)
            logger.info(f"Running Priority Management Agent for report {report_id}")
            priority_agent = PriorityManagementAgent(self.provider)
            priority_result = await priority_agent.execute(tasks=tasks_input or [], goals=goals)
            
            report.priority_analysis = priority_result
            report.progress = 50
            await db.commit()
            
            # 2. Meeting Prep Agent (50-100%)
            logger.info(f"Running Meeting Preparation Agent for report {report_id}")
            meeting_prep_agent = MeetingPreparationAgent(self.provider)
            meeting_briefs_result = []
            for meeting in (meetings_input or []):
                brief = await meeting_prep_agent.execute(
                    topic=meeting.get("topic", "Meeting"),
                    participants=meeting.get("participants"),
                    context=meeting.get("notes")
                )
                meeting_briefs_result.append({
                    "topic": meeting.get("topic"),
                    "participants": meeting.get("participants"),
                    "analysis": brief
                })
                
            report.meeting_briefs = meeting_briefs_result
            report.progress = 100
            report.status = "completed"
            report.completed_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"Workspace report analysis completed for {report_id}")
            return {
                "status": "completed",
                "report_id": str(report_id)
            }
            
        except Exception as e:
            logger.error(f"Error during workspace analysis for report {report_id}: {str(e)}", exc_info=True)
            stmt = select(Report).where(Report.id == report_id)
            result = await db.execute(stmt)
            report = result.scalar_one_or_none()
            if report:
                report.status = "failed"
                report.error_message = str(e)
                await db.commit()
            raise
