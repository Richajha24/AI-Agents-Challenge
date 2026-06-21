from pydantic import BaseModel, Field


class SWOTAnalysisRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=36)
    startup_concept: str = Field(min_length=1)


class SWOTAnalysisOutput(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]
    strategic_implications: list[str]
