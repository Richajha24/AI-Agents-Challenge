from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
import os

from database import engine, get_db, Base
from models import JobSearch, ResumeAnalysis, SkillGap, CoverLetter, InterviewPrep
from schemas import (
    JobSearchCreate, JobSearchResponse, ResumeUpload,
    ResumeAnalysisResponse, SkillGapResponse,
    CoverLetterResponse, InterviewPrepResponse, CompleteReport
)
from agents import JobSearchAgent, ResumeMatchAgent, SkillGapAgent, CoverLetterAgent, InterviewPrepAgent

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Hunter API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "job-hunter-api"}


@app.post("/api/search", response_model=JobSearchResponse)
def create_job_search(search: JobSearchCreate, db: Session = Depends(get_db)):
    """Create a new job search analysis"""
    job_search = JobSearch(**search.dict())
    db.add(job_search)
    db.commit()
    db.refresh(job_search)
    
    # Trigger async analysis (in production, use background tasks)
    # For now, we'll do it synchronously for simplicity
    try:
        job_search_agent = JobSearchAgent(provider="openai")
        result = job_search_agent.process(search.dict())
        job_search.status = "completed"
        db.commit()
    except Exception as e:
        job_search.status = "failed"
        db.commit()
    
    return job_search


@app.get("/api/search/{search_id}", response_model=JobSearchResponse)
def get_job_search(search_id: int, db: Session = Depends(get_db)):
    """Get job search status"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    return job_search


@app.post("/api/search/{search_id}/resume", response_model=ResumeAnalysisResponse)
def upload_resume(
    search_id: int,
    resume: ResumeUpload,
    db: Session = Depends(get_db)
):
    """Upload resume and get analysis"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    
    # Create or update resume analysis
    resume_analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.job_search_id == search_id
    ).first()
    
    if not resume_analysis:
        resume_analysis = ResumeAnalysis(
            job_search_id=search_id,
            resume_content=resume.resume_content
        )
        db.add(resume_analysis)
    else:
        resume_analysis.resume_content = resume.resume_content
    
    # Run resume match analysis
    try:
        resume_match_agent = ResumeMatchAgent(provider="openai")
        result = resume_match_agent.process({
            "resume_content": resume.resume_content,
            "job_description": "",
            "job_title": job_search.job_title,
            "skills": job_search.skills
        })
        
        resume_analysis.match_score = result.get("match_score")
        resume_analysis.missing_keywords = json.dumps(result.get("missing_keywords", []))
        resume_analysis.strengths = json.dumps(result.get("strengths", []))
        resume_analysis.weaknesses = json.dumps(result.get("weaknesses", []))
        resume_analysis.ats_suggestions = json.dumps(result.get("ats_suggestions", []))
        
        db.commit()
        db.refresh(resume_analysis)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    return resume_analysis


@app.get("/api/search/{search_id}/skill-gaps", response_model=SkillGapResponse)
def get_skill_gaps(search_id: int, db: Session = Depends(get_db)):
    """Get skill gap analysis"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    
    # Check if skill gap analysis exists
    skill_gap = db.query(SkillGap).filter(
        SkillGap.job_search_id == search_id
    ).first()
    
    if not skill_gap:
        # Create skill gap analysis
        resume_analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.job_search_id == search_id
        ).first()
        
        skill_gap = SkillGap(job_search_id=search_id)
        db.add(skill_gap)
        
        try:
            skill_gap_agent = SkillGapAgent(provider="openai")
            result = skill_gap_agent.process({
                "resume_content": resume_analysis.resume_content if resume_analysis else "",
                "target_role": job_search.job_title,
                "skills": job_search.skills
            })
            
            skill_gap.missing_skills = json.dumps(result.get("missing_skills", []))
            skill_gap.learning_roadmap = json.dumps(result.get("learning_roadmap", []))
            skill_gap.recommended_certifications = json.dumps(result.get("recommended_certifications", []))
            skill_gap.skill_priority = json.dumps(result.get("skill_priority", []))
            
            db.commit()
            db.refresh(skill_gap)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Skill gap analysis failed: {str(e)}")
    
    return skill_gap


@app.get("/api/search/{search_id}/cover-letter", response_model=CoverLetterResponse)
def get_cover_letter(search_id: int, company_name: str = "Target Company", db: Session = Depends(get_db)):
    """Get cover letter"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    
    # Check if cover letter exists
    cover_letter = db.query(CoverLetter).filter(
        CoverLetter.job_search_id == search_id,
        CoverLetter.company_name == company_name
    ).first()
    
    if not cover_letter:
        resume_analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.job_search_id == search_id
        ).first()
        
        if not resume_analysis:
            raise HTTPException(status_code=400, detail="Please upload resume first")
        
        cover_letter = CoverLetter(
            job_search_id=search_id,
            company_name=company_name
        )
        db.add(cover_letter)
        
        try:
            cover_letter_agent = CoverLetterAgent(provider="openai")
            result = cover_letter_agent.process({
                "resume_content": resume_analysis.resume_content,
                "job_description": "",
                "company_name": company_name,
                "job_title": job_search.job_title
            })
            
            cover_letter.cover_letter_content = result.get("cover_letter")
            cover_letter.talking_points = json.dumps(result.get("talking_points", []))
            cover_letter.personalization_suggestions = json.dumps(result.get("personalization_suggestions", []))
            
            db.commit()
            db.refresh(cover_letter)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")
    
    return cover_letter


@app.get("/api/search/{search_id}/interview", response_model=InterviewPrepResponse)
def get_interview_prep(search_id: int, company_name: str = "Target Company", db: Session = Depends(get_db)):
    """Get interview preparation"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    
    # Check if interview prep exists
    interview_prep = db.query(InterviewPrep).filter(
        InterviewPrep.job_search_id == search_id
    ).first()
    
    if not interview_prep:
        resume_analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.job_search_id == search_id
        ).first()
        
        interview_prep = InterviewPrep(job_search_id=search_id)
        db.add(interview_prep)
        
        try:
            interview_prep_agent = InterviewPrepAgent(provider="openai")
            result = interview_prep_agent.process({
                "job_description": "",
                "company_name": company_name,
                "resume_content": resume_analysis.resume_content if resume_analysis else "",
                "job_title": job_search.job_title,
                "skills": job_search.skills
            })
            
            interview_prep.interview_questions = json.dumps(result.get("interview_questions", []))
            interview_prep.technical_topics = json.dumps(result.get("technical_topics", []))
            interview_prep.behavioral_questions = json.dumps(result.get("behavioral_questions", []))
            interview_prep.star_answers = json.dumps(result.get("star_answers", []))
            interview_prep.preparation_roadmap = json.dumps(result.get("preparation_roadmap", []))
            
            db.commit()
            db.refresh(interview_prep)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Interview prep generation failed: {str(e)}")
    
    return interview_prep


@app.get("/api/search/{search_id}/report", response_model=CompleteReport)
def get_complete_report(search_id: int, db: Session = Depends(get_db)):
    """Get complete analysis report"""
    job_search = db.query(JobSearch).filter(JobSearch.id == search_id).first()
    if not job_search:
        raise HTTPException(status_code=404, detail="Job search not found")
    
    resume_analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.job_search_id == search_id
    ).first()
    
    skill_gap = db.query(SkillGap).filter(
        SkillGap.job_search_id == search_id
    ).first()
    
    cover_letter = db.query(CoverLetter).filter(
        CoverLetter.job_search_id == search_id
    ).first()
    
    interview_prep = db.query(InterviewPrep).filter(
        InterviewPrep.job_search_id == search_id
    ).first()
    
    return CompleteReport(
        job_search=job_search,
        resume_analysis=resume_analysis,
        skill_gaps=skill_gap,
        cover_letter=cover_letter,
        interview_prep=interview_prep
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
