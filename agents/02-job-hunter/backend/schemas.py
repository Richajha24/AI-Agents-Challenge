from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobSearchCreate(BaseModel):
    job_title: str = Field(..., description="Target job title")
    skills: str = Field(..., description="Comma-separated list of skills")
    experience: str = Field(..., description="Years of experience or level")
    location: str = Field(..., description="Preferred job location")


class JobSearchResponse(BaseModel):
    id: int
    job_title: str
    skills: str
    experience: str
    location: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeUpload(BaseModel):
    resume_content: str = Field(..., description="Resume text content")


class ResumeAnalysisResponse(BaseModel):
    id: int
    match_score: Optional[float]
    missing_keywords: Optional[str]
    strengths: Optional[str]
    weaknesses: Optional[str]
    ats_suggestions: Optional[str]

    class Config:
        from_attributes = True


class SkillGapResponse(BaseModel):
    id: int
    missing_skills: Optional[str]
    learning_roadmap: Optional[str]
    recommended_certifications: Optional[str]
    skill_priority: Optional[str]

    class Config:
        from_attributes = True


class CoverLetterResponse(BaseModel):
    id: int
    company_name: Optional[str]
    cover_letter_content: Optional[str]
    talking_points: Optional[str]
    personalization_suggestions: Optional[str]

    class Config:
        from_attributes = True


class InterviewPrepResponse(BaseModel):
    id: int
    interview_questions: Optional[str]
    technical_topics: Optional[str]
    behavioral_questions: Optional[str]
    star_answers: Optional[str]
    preparation_roadmap: Optional[str]

    class Config:
        from_attributes = True


class CompleteReport(BaseModel):
    job_search: JobSearchResponse
    resume_analysis: Optional[ResumeAnalysisResponse]
    skill_gaps: Optional[SkillGapResponse]
    cover_letter: Optional[CoverLetterResponse]
    interview_prep: Optional[InterviewPrepResponse]
