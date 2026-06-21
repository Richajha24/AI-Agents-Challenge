from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class LinkedInAnalysisInput(BaseModel):
    profile_url: str = Field(..., description="The LinkedIn profile URL")
    profile_info: Optional[str] = Field(None, description="Copy-pasted profile details/resume info")
    industry: str = Field(..., description="Target industry")
    career_goals: str = Field(..., description="Career goals")
    target_audience: str = Field(..., description="Target audience description")

class ProfileOptimizationResult(BaseModel):
    score: int
    headline_suggestions: List[str]
    about_improvements: str
    experience_optimization: str
    skills_recommendations: List[str]

class PersonalBrandResult(BaseModel):
    brand_identity: str
    positioning_statement: str
    content_pillars: List[str]
    audience_profile: str

class ContentStrategyResult(BaseModel):
    weekly_calendar: List[Dict[str, Any]]
    monthly_strategy: str
    content_themes: List[str]
    viral_opportunities: str

class PostGenerationResult(BaseModel):
    posts: List[Dict[str, Any]]
    hooks: List[str]

class GrowthRoadmapResult(BaseModel):
    thirty_day_plan: List[str]
    sixty_day_plan: List[str]
    ninety_day_plan: List[str]
    milestones: List[str]

class AnalysisResult(BaseModel):
    analysis_id: UUID
    status: str
    progress: int
    profile_url: str
    industry: str
    career_goals: str
    target_audience: str
    profile_score: Optional[int] = None
    profile_optimization: Optional[ProfileOptimizationResult] = None
    personal_brand: Optional[PersonalBrandResult] = None
    content_strategy: Optional[ContentStrategyResult] = None
    post_generation: Optional[PostGenerationResult] = None
    growth_roadmap: Optional[GrowthRoadmapResult] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class AnalysisStatusResponse(BaseModel):
    analysis_id: UUID
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime
