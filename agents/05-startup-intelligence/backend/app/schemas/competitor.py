from pydantic import BaseModel, Field


class CompetitorAnalysisRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=36)
    industry: str = Field(min_length=1)
    competitor_names: list[str] = Field(min_length=1)


class CompetitorProfile(BaseModel):
    name: str
    positioning: str
    strengths: list[str]
    weaknesses: list[str]


class CompetitorIntelligenceOutput(BaseModel):
    competitor_analysis: list[CompetitorProfile]
    competitive_landscape: str
    differentiation_insights: list[str]
