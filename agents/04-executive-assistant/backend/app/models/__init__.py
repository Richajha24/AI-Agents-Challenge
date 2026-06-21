from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from datetime import datetime
import uuid
from app.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    progress = Column(Integer, default=0)
    goals = Column(Text, nullable=True)
    
    # Inputs
    tasks_input = Column(JSON, nullable=True)
    meetings_input = Column(JSON, nullable=True)
    
    # Agent Outputs
    priority_analysis = Column(JSON, nullable=True)
    meeting_briefs = Column(JSON, nullable=True)
    daily_roadmap = Column(JSON, nullable=True)
    
    # Errors and Metadata
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    problem_statement = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    analysis_result = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
