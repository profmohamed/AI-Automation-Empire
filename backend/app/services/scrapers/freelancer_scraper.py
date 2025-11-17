"""
Freelancer.com job scraper
"""
from typing import Dict, List, Any
from loguru import logger
from .playwright_scraper import PlaywrightScraper


class FreelancerScraper(PlaywrightScraper):
    """Scraper for Freelancer.com"""

    BASE_URL = "https://www.freelancer.com"

    async def scrape_jobs(self, keywords: str = "", max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape Freelancer jobs"""
        search_url = f"{self.BASE_URL}/jobs?keyword={keywords.replace(' ', '+')}"
        logger.info(f"Scraping Freelancer jobs: {search_url}")

        return await self.scrape(
            url=search_url,
            max_pages=max_pages,
            scroll_to_load=True,
            wait_for_selector=".JobSearchCard-item",
        )

    async def extract_data(self, page) -> List[Dict[str, Any]]:
        """Extract job listings"""
        jobs = []
        job_elements = await page.query_selector_all(".JobSearchCard-item")

        for element in job_elements:
            try:
                job = {}
                title_el = await element.query_selector(".JobSearchCard-primary-heading-link")
                if title_el:
                    job["title"] = await title_el.inner_text()
                    href = await title_el.get_attribute("href")
                    job["url"] = f"{self.BASE_URL}{href}" if href else None

                desc_el = await element.query_selector(".JobSearchCard-primary-description")
                if desc_el:
                    job["description"] = await desc_el.inner_text()

                budget_el = await element.query_selector(".JobSearchCard-primary-price")
                if budget_el:
                    job["budget"] = await budget_el.inner_text()

                job["platform"] = "freelancer"
                jobs.append(job)
            except Exception as e:
                logger.warning(f"Error parsing Freelancer job: {e}")

        return jobs

    def parse_item(self, element: Any) -> Dict[str, Any]:
        return {}
