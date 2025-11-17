"""
Proposal model
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class ProposalStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    SENT = "sent"
    VIEWED = "viewed"
    RESPONDED = "responded"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Proposal(Base):
    """Proposal model for AI-generated proposals"""

    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))

    # Content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    short_pitch = Column(Text)  # Elevator pitch
    cover_letter = Column(Text)

    # Pricing
    proposed_budget = Column(Float)
    proposed_timeline = Column(String)
    milestones = Column(JSON)  # Array of milestone objects

    # AI Generation Info
    ai_model_used = Column(String)
    generation_prompt = Column(Text)
    generation_tokens = Column(Integer)
    ai_confidence_score = Column(Float)  # 0-1

    # Customization
    template_id = Column(Integer)
    is_customized = Column(Boolean, default=False)
    customization_notes = Column(Text)

    # Status & Tracking
    status = Column(SQLEnum(ProposalStatus), default=ProposalStatus.DRAFT, index=True)
    sent_at = Column(DateTime(timezone=True))
    viewed_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))

    # Follow-ups
    follow_up_count = Column(Integer, default=0)
    next_follow_up = Column(DateTime(timezone=True))
    auto_follow_up_enabled = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="proposals")
    opportunity = relationship("Opportunity", back_populates="proposals")
    client = relationship("Client", back_populates="proposals")
