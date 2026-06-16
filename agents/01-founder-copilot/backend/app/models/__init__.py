from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=True)
    startup_idea = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    problem_statement = Column(Text, nullable=False)
    website_url = Column(String, nullable=True)
    
    # Analysis results
    idea_analysis = Column(JSON, nullable=True)
    competitor_analysis = Column(JSON, nullable=True)
    market_research = Column(JSON, nullable=True)
    customer_personas = Column(JSON, nullable=True)
    mvp_plan = Column(JSON, nullable=True)
    pricing_strategy = Column(JSON, nullable=True)
    go_to_market = Column(JSON, nullable=True)
    execution_roadmap = Column(JSON, nullable=True)
    
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
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    pdf_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
