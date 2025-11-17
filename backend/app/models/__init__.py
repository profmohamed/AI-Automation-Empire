"""
Database models for AI Automation Empire
"""
from .user import User
from .opportunity import Opportunity
from .client import Client
from .proposal import Proposal
from .outreach import OutreachLog, OutreachCampaign
from .scraping import ScrapingJob, ScrapingLog
from .subscription import Subscription, UsageLog

__all__ = [
    "User",
    "Opportunity",
    "Client",
    "Proposal",
    "OutreachLog",
    "OutreachCampaign",
    "ScrapingJob",
    "ScrapingLog",
    "Subscription",
    "UsageLog",
]
