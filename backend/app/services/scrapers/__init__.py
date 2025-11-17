"""
Scraping services
"""
from .base_scraper import BaseScraper
from .playwright_scraper import PlaywrightScraper
from .upwork_scraper import UpworkScraper
from .linkedin_scraper import LinkedInScraper
from .indeed_scraper import IndeedScraper
from .freelancer_scraper import FreelancerScraper

__all__ = [
    "BaseScraper",
    "PlaywrightScraper",
    "UpworkScraper",
    "LinkedInScraper",
    "IndeedScraper",
    "FreelancerScraper",
]
