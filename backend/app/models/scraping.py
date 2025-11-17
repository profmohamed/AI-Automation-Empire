"""
Scraping models for tracking scraping jobs and logs
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class ScrapingStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class ScrapingPlatform(str, enum.Enum):
    UPWORK = "upwork"
    FREELANCER = "freelancer"
    FIVERR = "fiverr"
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GITHUB_JOBS = "github_jobs"
    REMOTE_CO = "remote_co"
    WEWORKREMOTELY = "weworkremotely"
    AMAZON = "amazon"
    EBAY = "ebay"
    ETSY = "etsy"
    CUSTOM = "custom"


class ScrapingJob(Base):
    """Scraping job configuration and tracking"""

    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Job configuration
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    platform = Column(SQLEnum(ScrapingPlatform), nullable=False, index=True)
    target_url = Column(String, nullable=False)

    # Scraping config
    scraping_config = Column(JSON)  # Selectors, pagination, etc.
    max_pages = Column(Integer, default=10)
    max_items = Column(Integer, default=100)
    delay_between_requests = Column(Float, default=2.0)

    # Filters
    filters = Column(JSON)  # Search filters, keywords, etc.
    keywords = Column(JSON)  # Array of keywords to search

    # Schedule
    is_scheduled = Column(Boolean, default=False)
    schedule_cron = Column(String)  # Cron expression
    run_frequency = Column(String)  # hourly, daily, weekly, etc.
    next_run = Column(DateTime(timezone=True))
    last_run = Column(DateTime(timezone=True))

    # Status
    status = Column(SQLEnum(ScrapingStatus), default=ScrapingStatus.PENDING, index=True)
    is_active = Column(Boolean, default=True)

    # Statistics
    total_runs = Column(Integer, default=0)
    total_items_scraped = Column(Integer, default=0)
    total_success = Column(Integer, default=0)
    total_failures = Column(Integer, default=0)
    success_rate = Column(Float)  # 0-1

    # Performance
    average_duration = Column(Float)  # seconds
    last_duration = Column(Float)  # seconds

    # Proxy & Anti-bot
    use_proxy = Column(Boolean, default=False)
    proxy_list = Column(JSON)
    use_captcha_solver = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="scraping_jobs")
    scraping_logs = relationship("ScrapingLog", back_populates="job", cascade="all, delete-orphan")


class ScrapingLog(Base):
    """Individual scraping execution log"""

    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("scraping_jobs.id"), nullable=False, index=True)

    # Execution info
    started_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True))
    duration = Column(Float)  # seconds

    # Status
    status = Column(SQLEnum(ScrapingStatus), default=ScrapingStatus.RUNNING, index=True)
    error_message = Column(Text)
    error_traceback = Column(Text)

    # Results
    items_found = Column(Integer, default=0)
    items_processed = Column(Integer, default=0)
    items_saved = Column(Integer, default=0)
    items_duplicates = Column(Integer, default=0)
    pages_scraped = Column(Integer, default=0)

    # Performance
    requests_made = Column(Integer, default=0)
    requests_failed = Column(Integer, default=0)
    captchas_solved = Column(Integer, default=0)
    proxies_used = Column(Integer, default=0)

    # Data
    sample_data = Column(JSON)  # Sample of scraped items
    statistics = Column(JSON)  # Additional statistics

    # Metadata
    metadata = Column(JSON)  # Additional execution metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    job = relationship("ScrapingJob", back_populates="scraping_logs")
