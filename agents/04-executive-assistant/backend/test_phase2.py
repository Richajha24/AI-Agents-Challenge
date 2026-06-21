import asyncio
import sys
import os

# Insert current directory into path
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, AsyncSessionLocal
from app.config import settings
from app.ai.provider import get_provider
from app.agents.priority import PriorityManagementAgent
from app.agents.meeting_prep import MeetingPreparationAgent
from app.models import Report
from sqlalchemy import select

client = TestClient(app)

async def test_direct_agents():
    print("\n--- 1. Testing Agents Directly with AI Provider ---")
    provider_key_map = {
        "gemini": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
    }
    api_key = getattr(settings, provider_key_map.get(settings.DEFAULT_PROVIDER.lower(), ""), None)
    if not api_key:
        print(f"Error: API key for {settings.DEFAULT_PROVIDER} not found.")
        sys.exit(1)
        
    print(f"Using AI provider: {settings.DEFAULT_PROVIDER}")
    provider = get_provider(settings.DEFAULT_PROVIDER, api_key)
    
    # Priority Management Agent
    print("\nTesting PriorityManagementAgent...")
    priority_agent = PriorityManagementAgent(provider)
    tasks = [
        {"title": "Review marketing materials", "description": "Check colors and copy", "category": "Marketing"},
        {"title": "Bug fix in payment gateway", "description": "Crash when card is declined", "category": "Engineering", "deadline": "Today"}
    ]
    goals = "Launch beta version by Friday, secure payment infrastructure."
    priority_res = await priority_agent.execute(tasks=tasks, goals=goals)
    
    print("Priority Management Output keys:", list(priority_res.keys()))
    print("Critical Path:", priority_res.get("critical_path"))
    assert "priority_ranking" in priority_res, "priority_ranking missing"
    assert "focus_recommendations" in priority_res, "focus_recommendations missing"
    assert "critical_path" in priority_res, "critical_path missing"
    print("✓ PriorityManagementAgent direct test passed!")
    
    # Meeting Prep Agent
    print("\nTesting MeetingPreparationAgent...")
    meeting_agent = MeetingPreparationAgent(provider)
    meeting_res = await meeting_agent.execute(
        topic="Product alignment with CTO",
        participants="CTO, Lead Designer",
        context="Aligning design system changes and release timelines for payment gateway update."
    )
    print("Meeting Prep Output keys:", list(meeting_res.keys()))
    print("Brief:", meeting_res.get("brief"))
    assert "brief" in meeting_res, "brief missing"
    assert "agenda" in meeting_res, "agenda missing"
    assert "discussion_points" in meeting_res, "discussion_points missing"
    assert "risk_areas" in meeting_res, "risk_areas missing"
    print("✓ MeetingPreparationAgent direct test passed!")


def test_api_endpoints():
    print("\n--- 2. Testing API Endpoints via TestClient ---")
    
    # Initialize DB (run once before endpoints test)
    # TestClient will trigger lifespan, which runs init_db()
    
    # Test /api/tasks/analyze
    print("\nTesting POST /api/tasks/analyze...")
    payload = {
        "tasks": [
            {"title": "Prepare slide deck", "category": "Sales"},
            {"title": "Setup server monitoring", "category": "Devops"}
        ],
        "goals": "Increase system reliability and close client deal."
    }
    response = client.post("/api/tasks/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    res_data = response.json()
    assert "priority_ranking" in res_data
    print("✓ POST /api/tasks/analyze endpoint passed!")
    
    # Test /api/meetings/prepare
    print("\nTesting POST /api/meetings/prepare...")
    payload = {
        "topic": "Investor Pitch Prep",
        "participants": "CEO, CFO",
        "context": "Reviewing financial deck before meeting Series A VCs."
    }
    response = client.post("/api/meetings/prepare", json=payload)
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    res_data = response.json()
    assert "brief" in res_data
    print("✓ POST /api/meetings/prepare endpoint passed!")


async def test_workspace_orchestration_and_db():
    print("\n--- 3. Testing Full Report Generation & Database Writes ---")
    
    payload = {
        "goals": "Fix payment bugs, prepare for CTO sync.",
        "tasks_input": [
            {"title": "Bug fix in payment gateway", "description": "Crash when card is declined", "category": "Engineering", "deadline": "Today"}
        ],
        "meetings_input": [
            {"topic": "Product alignment with CTO", "participants": "CTO, Lead Designer", "notes": "CTO sync"}
        ]
    }
    
    print("\nSending POST /api/report/generate...")
    response = client.post("/api/report/generate", json=payload)
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200
    res_data = response.json()
    report_id = res_data.get("report_id")
    print(f"Report ID generated: {report_id}")
    assert report_id is not None
    
    # Verify the database write and background task completion
    print("\nVerifying database writes for Report...")
    async with AsyncSessionLocal() as db:
        stmt = select(Report).where(Report.id == report_id)
        db_res = await db.execute(stmt)
        report = db_res.scalar_one_or_none()
        
        assert report is not None, "Report was not written to the database"
        print(f"Initial DB Status: {report.status}, Progress: {report.progress}%")
        
        # TestClient runs background tasks synchronously. Let's poll or fetch via GET endpoint to see completed state.
        print("\nFetching Report via GET /api/report/{id}...")
        get_response = client.get(f"/api/report/{report_id}")
        assert get_response.status_code == 200
        get_data = get_response.json()
        print(f"GET Status: {get_data.get('status')}, Progress: {get_data.get('progress')}%")
        
        assert get_data.get("status") == "completed", f"Status expected completed, got {get_data.get('status')}"
        assert get_data.get("progress") == 100
        assert get_data.get("priority_analysis") is not None, "priority_analysis is missing in DB report"
        assert get_data.get("meeting_briefs") is not None, "meeting_briefs is missing in DB report"
        
        print("\nDatabase report outputs:")
        print("Priority Analysis focus:", get_data.get("priority_analysis").get("focus_recommendations"))
        print("Meeting Brief topic:", get_data.get("meeting_briefs")[0].get("topic"))
        
    print("✓ Full Report Generation & Database writes verification passed!")


async def run_all():
    print("Starting Phase 2 verification...")
    # Initialize DB tables for testing
    await init_db()
    
    await test_direct_agents()
    test_api_endpoints()
    await test_workspace_orchestration_and_db()
    
    print("\n==========================================")
    print("ALL PHASE 2 VERIFICATIONS PASSED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(run_all())
