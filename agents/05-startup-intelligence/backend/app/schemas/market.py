from pydantic import BaseModel, Field


class MarketAnalysisRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=36)
    industry: str = Field(min_length=1)
    startup_idea: str = Field(min_length=1)


class MarketIntelligenceOutput(BaseModel):
    market_overview: str
    growth_indicators: list[str]
    opportunity_areas: list[str]
    market_size_context: str
    key_assumptions: list[str]
