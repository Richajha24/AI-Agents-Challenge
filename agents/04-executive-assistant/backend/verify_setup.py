import asyncio
import sys
import os

# Insert current directory into path
sys.path.insert(0, '.')

async def main():
    print("Verifying backend foundation imports...")
    try:
        from app.config import settings
        from app.database import init_db, get_db
        from app.models import Report, Decision
        from app.schemas import WorkspaceInput, ReportResult
        from app.ai.provider import get_provider
        from app.agents.priority import PriorityManagementAgent
        from app.agents.meeting_prep import MeetingPreparationAgent
        from app.agents.daily_planner import DailyPlannerAgent
        from app.agents.decision import DecisionSupportAgent
        from app.orchestrator import ExecutiveAssistantOrchestrator
        from app.api.routes import router
        
        print("[OK] All imports successful!")
        
        # Test database initialization
        print("Initializing database...")
        await init_db()
        print("[OK] Database initialized successfully!")
        
        # Check if database file exists
        db_path = "./executive_assistant.db"
        if os.path.exists(db_path):
            print(f"[OK] Database file found at {db_path} ({os.path.getsize(db_path)} bytes)")
        else:
            print("[ERROR] Database file not found!")
            sys.exit(1)
            
        print("[OK] Verification completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
