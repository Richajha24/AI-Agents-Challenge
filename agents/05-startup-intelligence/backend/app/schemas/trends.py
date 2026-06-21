from pydantic import BaseModel, Field


class TrendDiscoveryRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=36)
    industry: str = Field(min_length=1)


class TrendItem(BaseModel):
    trend: str
    description: str
    maturity: str
    relevance: str


class TrendDiscoveryOutput(BaseModel):
    emerging_trends: list[TrendItem]
    technology_shifts: list[str]
    growth_sectors: list[str]
    watch_signals: list[str]
