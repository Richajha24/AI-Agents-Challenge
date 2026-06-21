from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

# Input schemas
class TaskInput(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task details")
    deadline: Optional[str] = Field(None, description="Deadline or due date")
    category: Optional[str] = Field(None, description="Category of work")

class MeetingInput(BaseModel):
    topic: str = Field(..., description="Meeting topic/title")
    participants: Optional[str] = Field(None, description="List of participants")
    time: Optional[str] = Field(None, description="Time of the meeting")
    notes: Optional[str] = Field(None, description="Any pre-meeting context or notes")

class WorkspaceInput(BaseModel):
    goals: Optional[str] = Field(None, description="Main goals or focus for the day/week")
    tasks_input: List[TaskInput] = Field(default=[], description="List of tasks to analyze")
    meetings_input: List[MeetingInput] = Field(default=[], description="List of meetings to prepare for")

class DecisionInput(BaseModel):
    problem_statement: str = Field(..., description="The decision dilemma or problem statement")
    options: List[str] = Field(..., description="List of options being considered")

# Individual API endpoint inputs for Phase 1 / individual widget calls
class TasksAnalyzeInput(BaseModel):
    tasks: List[TaskInput]
    goals: Optional[str] = None

class MeetingPrepareInput(BaseModel):
    topic: str
    participants: Optional[str] = None
    context: Optional[str] = None

class DecisionAnalyzeInput(BaseModel):
    problem_statement: str
    options: List[str]

# Detailed Output sub-schemas
class PriorityAnalysisResult(BaseModel):
    priority_ranking: List[Dict[str, Any]] = Field(..., description="Ranked tasks list")
    focus_recommendations: List[str] = Field(..., description="Focus guidelines")
    critical_path: List[str] = Field(..., description="Critical path items")

class MeetingPrepResult(BaseModel):
    brief: str = Field(..., description="Meeting overview brief")
    agenda: List[str] = Field(..., description="Proposed agenda")
    discussion_points: List[str] = Field(..., description="Key points to bring up")
    risk_areas: List[str] = Field(..., description="Risks or caveats")

class DailyRoadmapResult(BaseModel):
    daily_roadmap: List[Dict[str, Any]] = Field(..., description="Suggested timeline/schedule")
    deep_work_blocks: List[Dict[str, Any]] = Field(..., description="Focus blocks")
    focus_recommendations: List[str] = Field(..., description="How to maximize productivity")

class DecisionSupportResult(BaseModel):
    pros_and_cons: Dict[str, Dict[str, Any]] = Field(..., description="Pros & Cons for each option")
    risk_analysis: Dict[str, List[str]] = Field(..., description="Risks associated with options")
    decision_framework: str = Field(..., description="Criteria and weighting details")
    recommendation: str = Field(..., description="Recommended option and rationale")

# API response wrappers
class ReportStatusResponse(BaseModel):
    report_id: str
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime

class ReportResult(BaseModel):
    report_id: str
    status: str
    progress: int
    goals: Optional[str] = None
    tasks_input: List[Dict[str, Any]] = []
    meetings_input: List[Dict[str, Any]] = []
    priority_analysis: Optional[Dict[str, Any]] = None
    meeting_briefs: Optional[List[Dict[str, Any]]] = None  # Briefs for all prepared meetings
    daily_roadmap: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class DecisionResult(BaseModel):
    decision_id: str
    problem_statement: str
    options: List[str]
    analysis_result: Optional[Dict[str, Any]] = None
    created_at: datetime
