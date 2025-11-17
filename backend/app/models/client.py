"""
Client model
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Client(Base):
    """Client model for storing client information"""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic info
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    company = Column(String, index=True)
    website = Column(String)

    # Location
    location = Column(String)
    country = Column(String, index=True)
    timezone = Column(String)

    # Social & Contact
    linkedin_url = Column(String)
    twitter_url = Column(String)
    facebook_url = Column(String)

    # Business Info
    industry = Column(String, index=True)
    company_size = Column(String)
    annual_revenue = Column(String)

    # AI Analysis
    client_score = Column(Float)  # 0-100, likelihood to convert
    interests = Column(JSON)  # Array of interests
    pain_points = Column(JSON)  # Identified pain points
    budget_range = Column(String)
    preferred_contact_method = Column(String)

    # Interaction history
    total_opportunities = Column(Integer, default=0)
    total_proposals_sent = Column(Integer, default=0)
    total_messages_sent = Column(Integer, default=0)
    last_contacted = Column(DateTime(timezone=True))
    response_rate = Column(Float)  # 0-1

    # Status
    is_active = Column(Boolean, default=True)
    is_blacklisted = Column(Boolean, default=False)
    blacklist_reason = Column(Text)

    # Metadata
    notes = Column(Text)
    custom_fields = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="clients")
    opportunities = relationship("Opportunity", back_populates="client")
    proposals = relationship("Proposal", back_populates="client")
    outreach_logs = relationship("OutreachLog", back_populates="client", cascade="all, delete-orphan")
