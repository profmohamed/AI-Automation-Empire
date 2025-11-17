"""
Subscription and usage models for SaaS features
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    UNPAID = "unpaid"


class UsageType(str, enum.Enum):
    SCRAPING = "scraping"
    AI_TOKENS = "ai_tokens"
    OUTREACH = "outreach"
    PROPOSAL_GENERATION = "proposal_generation"
    API_CALL = "api_call"


class Subscription(Base):
    """User subscription model"""

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Subscription info
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, index=True)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, index=True)

    # Stripe info
    stripe_customer_id = Column(String, unique=True, index=True)
    stripe_subscription_id = Column(String, unique=True, index=True)
    stripe_price_id = Column(String)

    # Billing
    current_period_start = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    cancel_at_period_end = Column(Boolean, default=False)
    cancelled_at = Column(DateTime(timezone=True))

    # Usage limits (per month)
    scraping_limit = Column(Integer, default=100)
    ai_tokens_limit = Column(Integer, default=10000)
    outreach_limit = Column(Integer, default=50)
    proposals_limit = Column(Integer, default=10)

    # Current usage (resets monthly)
    scraping_used = Column(Integer, default=0)
    ai_tokens_used = Column(Integer, default=0)
    outreach_used = Column(Integer, default=0)
    proposals_used = Column(Integer, default=0)

    # Trial info
    trial_start = Column(DateTime(timezone=True))
    trial_end = Column(DateTime(timezone=True))
    is_trial = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="subscription")


class UsageLog(Base):
    """Detailed usage tracking"""

    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Usage details
    usage_type = Column(SQLEnum(UsageType), nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # Number of units used
    cost = Column(Float)  # Cost in credits or dollars

    # Context
    resource_id = Column(Integer)  # ID of related resource (job_id, campaign_id, etc.)
    resource_type = Column(String)  # Type of resource
    description = Column(Text)

    # Metadata
    metadata = Column(JSON)  # Additional usage data
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="usage_logs")
