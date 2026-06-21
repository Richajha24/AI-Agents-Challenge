from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from datetime import datetime
import uuid
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    profile_url = Column(String, nullable=False)
    profile_info = Column(Text, nullable=True)
    industry = Column(String, nullable=False)
    career_goals = Column(Text, nullable=False)
    target_audience = Column(String, nullable=False)
    
    # Analysis results
    profile_score = Column(Integer, nullable=True)
    profile_optimization = Column(JSON, nullable=True)
    personal_brand = Column(JSON, nullable=True)
    content_strategy = Column(JSON, nullable=True)
    post_generation = Column(JSON, nullable=True)
    growth_roadmap = Column(JSON, nullable=True)
    
    # Status
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    progress = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String(36), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
