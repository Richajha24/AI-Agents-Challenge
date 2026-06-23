from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class JobSearch(Base):
    __tablename__ = "job_searches"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    skills = Column(Text, nullable=False)
    experience = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume_analysis = relationship("ResumeAnalysis", back_populates="job_search", uselist=False)
    skill_gaps = relationship("SkillGap", back_populates="job_search")
    cover_letters = relationship("CoverLetter", back_populates="job_search")
    interview_preps = relationship("InterviewPrep", back_populates="job_search")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    job_search_id = Column(Integer, ForeignKey("job_searches.id"))
    resume_content = Column(Text)
    match_score = Column(Float)
    missing_keywords = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    ats_suggestions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job_search = relationship("JobSearch", back_populates="resume_analysis")


class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(Integer, primary_key=True, index=True)
    job_search_id = Column(Integer, ForeignKey("job_searches.id"))
    missing_skills = Column(Text)
    learning_roadmap = Column(Text)
    recommended_certifications = Column(Text)
    skill_priority = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job_search = relationship("JobSearch", back_populates="skill_gaps")


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    job_search_id = Column(Integer, ForeignKey("job_searches.id"))
    company_name = Column(String)
    cover_letter_content = Column(Text)
    talking_points = Column(Text)
    personalization_suggestions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job_search = relationship("JobSearch", back_populates="cover_letters")


class InterviewPrep(Base):
    __tablename__ = "interview_preps"

    id = Column(Integer, primary_key=True, index=True)
    job_search_id = Column(Integer, ForeignKey("job_searches.id"))
    interview_questions = Column(Text)
    technical_topics = Column(Text)
    behavioral_questions = Column(Text)
    star_answers = Column(Text)
    preparation_roadmap = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    job_search = relationship("JobSearch", back_populates="interview_preps")
