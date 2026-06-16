from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class StartupIdeaInput(BaseModel):
    startup_idea: str = Field(..., description="The startup idea or product concept")
    industry: str = Field(..., description="Industry/market")
    problem_statement: str = Field(..., description="Problem being solved")
    website_url: Optional[str] = Field(None, description="Optional website for research")

class IdeaAnalysisResult(BaseModel):
    problem_summary: str
    opportunity_assessment: str
    market_attractiveness_score: int
    risk_assessment: str
    key_insights: List[str]

class CompetitorAnalysisResult(BaseModel):
    direct_competitors: List[Dict[str, Any]]
    indirect_competitors: List[Dict[str, Any]]
    comparison_table: Dict[str, Any]
    differentiation_opportunities: List[str]

class MarketResearchResult(BaseModel):
    tam: str  # Total Addressable Market
    sam: str  # Serviceable Available Market
    som: str  # Serviceable Obtainable Market
    market_size_estimate: str
    industry_trends: List[str]
    growth_opportunities: List[str]

class CustomerPersonaResult(BaseModel):
    personas: List[Dict[str, Any]]
    primary_pain_points: List[str]
    buying_motivations: List[str]
    behavioral_patterns: List[str]

class MVPPlanResult(BaseModel):
    core_features: List[str]
    nice_to_have_features: List[str]
    development_priorities: List[Dict[str, Any]]
    estimated_timeline: str

class PricingStrategyResult(BaseModel):
    subscription_models: List[Dict[str, Any]]
    freemium_option: Optional[Dict[str, Any]]
    enterprise_pricing: Optional[Dict[str, Any]]
    recommended_pricing: str

class GoToMarketResult(BaseModel):
    launch_strategy: str
    acquisition_channels: List[str]
    content_strategy: List[str]
    distribution_strategy: str

class ExecutionRoadmapResult(BaseModel):
    thirty_day_plan: Dict[str, Any]
    sixty_day_plan: Dict[str, Any]
    ninety_day_plan: Dict[str, Any]
    six_month_plan: Dict[str, Any]
    one_year_plan: Dict[str, Any]

class AnalysisResult(BaseModel):
    analysis_id: UUID
    status: str
    progress: int
    startup_idea: str
    industry: str
    idea_analysis: Optional[IdeaAnalysisResult] = None
    competitor_analysis: Optional[CompetitorAnalysisResult] = None
    market_research: Optional[MarketResearchResult] = None
    customer_personas: Optional[CustomerPersonaResult] = None
    mvp_plan: Optional[MVPPlanResult] = None
    pricing_strategy: Optional[PricingStrategyResult] = None
    go_to_market: Optional[GoToMarketResult] = None
    execution_roadmap: Optional[ExecutionRoadmapResult] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class AnalysisStatusResponse(BaseModel):
    analysis_id: UUID
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime
