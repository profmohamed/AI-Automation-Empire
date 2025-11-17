"""
Outreach models for communication tracking
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class OutreachChannel(str, enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    TELEGRAM = "telegram"
    SMS = "sms"
    DIRECT_MESSAGE = "direct_message"


class OutreachStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    BOUNCED = "bounced"
    FAILED = "failed"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class OutreachCampaign(Base):
    """Outreach campaign for organizing communication efforts"""

    __tablename__ = "outreach_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic info
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    channel = Column(SQLEnum(OutreachChannel), nullable=False)

    # Configuration
    template_id = Column(Integer)
    auto_send = Column(Boolean, default=False)
    send_schedule = Column(JSON)  # Schedule configuration
    daily_limit = Column(Integer, default=50)

    # Follow-up sequence
    follow_up_enabled = Column(Boolean, default=True)
    follow_up_delay_days = Column(Integer, default=3)
    max_follow_ups = Column(Integer, default=3)
    follow_up_templates = Column(JSON)  # Array of template IDs

    # Targeting
    target_filters = Column(JSON)  # Filter criteria
    target_count = Column(Integer, default=0)

    # Statistics
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_clicked = Column(Integer, default=0)
    total_replied = Column(Integer, default=0)
    total_failed = Column(Integer, default=0)

    # Status
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="campaigns")
    outreach_logs = relationship("OutreachLog", back_populates="campaign", cascade="all, delete-orphan")


class OutreachLog(Base):
    """Individual outreach log entry"""

    __tablename__ = "outreach_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("outreach_campaigns.id"))
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Message details
    channel = Column(SQLEnum(OutreachChannel), nullable=False, index=True)
    subject = Column(String)
    message = Column(Text, nullable=False)
    message_id = Column(String)  # External message ID (email ID, etc.)

    # Recipient
    recipient_email = Column(String)
    recipient_phone = Column(String)
    recipient_username = Column(String)

    # Status
    status = Column(SQLEnum(OutreachStatus), default=OutreachStatus.PENDING, index=True)
    error_message = Column(Text)

    # Tracking
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    opened_at = Column(DateTime(timezone=True))
    clicked_at = Column(DateTime(timezone=True))
    replied_at = Column(DateTime(timezone=True))

    # Response
    reply_content = Column(Text)
    reply_sentiment = Column(String)  # positive, neutral, negative

    # Follow-up
    is_follow_up = Column(Boolean, default=False)
    parent_log_id = Column(Integer, ForeignKey("outreach_logs.id"))
    follow_up_number = Column(Integer, default=0)

    # Metadata
    metadata = Column(JSON)  # Additional tracking data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("OutreachCampaign", back_populates="outreach_logs")
    client = relationship("Client", back_populates="outreach_logs")
    parent_log = relationship("OutreachLog", remote_side=[id], backref="follow_ups")
