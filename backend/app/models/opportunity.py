"""
Opportunity model for scraped jobs and leads
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class OpportunityType(str, enum.Enum):
    JOB = "job"
    FREELANCE_GIG = "freelance_gig"
    PRODUCT = "product"
    LEAD = "lead"
    PARTNERSHIP = "partnership"


class OpportunityStatus(str, enum.Enum):
    NEW = "new"
    ANALYZED = "analyzed"
    CONTACTED = "contacted"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    IGNORED = "ignored"


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class Opportunity(Base):
    """Opportunity model for scraped opportunities"""

    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic info
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    source_url = Column(String)
    source_platform = Column(String, index=True)  # upwork, freelancer, linkedin, etc.

    # Classification
    opportunity_type = Column(SQLEnum(OpportunityType), default=OpportunityType.JOB)
    status = Column(SQLEnum(OpportunityStatus), default=OpportunityStatus.NEW, index=True)
    category = Column(String, index=True)  # web-dev, design, marketing, etc.
    tags = Column(JSON)  # Array of tags

    # Budget & Pricing
    budget_min = Column(Float)
    budget_max = Column(Float)
    budget_currency = Column(String, default="USD")
    is_fixed_price = Column(Boolean, default=False)
    hourly_rate = Column(Float)

    # AI Analysis
    difficulty = Column(SQLEnum(DifficultyLevel))
    ai_score = Column(Float)  # 0-100 score from AI
    pain_points = Column(JSON)  # Extracted pain points
    keywords = Column(JSON)  # Extracted keywords
    sentiment_score = Column(Float)  # -1 to 1
    ai_summary = Column(Text)
    required_skills = Column(JSON)

    # Client reference
    client_id = Column(Integer, ForeignKey("clients.id"))

    # Client info (cached for quick access)
    client_name = Column(String)
    client_email = Column(String)
    client_phone = Column(String)
    client_company = Column(String)
    client_location = Column(String)

    # Metadata
    posted_at = Column(DateTime(timezone=True))
    deadline = Column(DateTime(timezone=True))
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Raw data
    raw_data = Column(JSON)  # Store full scraped data

    # Relationships
    user = relationship("User", back_populates="opportunities")
    proposals = relationship("Proposal", back_populates="opportunity", cascade="all, delete-orphan")
    client = relationship("Client", back_populates="opportunities")
