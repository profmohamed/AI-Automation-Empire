"""
Indeed job scraper
"""
from typing import Dict, List, Any
from loguru import logger
from .playwright_scraper import PlaywrightScraper


class IndeedScraper(PlaywrightScraper):
    """Scraper for Indeed jobs"""

    BASE_URL = "https://www.indeed.com"

    async def scrape_jobs(self, keywords: str = "", location: str = "", max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape Indeed jobs"""
        search_url = f"{self.BASE_URL}/jobs?q={keywords.replace(' ', '+')}&l={location.replace(' ', '+')}"
        logger.info(f"Scraping Indeed jobs: {search_url}")

        return await self.scrape(
            url=search_url,
            max_pages=max_pages,
            scroll_to_load=True,
            wait_for_selector=".job_seen_beacon",
        )

    async def extract_data(self, page) -> List[Dict[str, Any]]:
        """Extract job listings"""
        jobs = []
        job_elements = await page.query_selector_all(".job_seen_beacon")

        for element in job_elements:
            try:
                job = {}
                title_el = await element.query_selector("h2.jobTitle")
                if title_el:
                    job["title"] = await title_el.inner_text()

                company_el = await element.query_selector("[data-testid='company-name']")
                if company_el:
                    job["company"] = await company_el.inner_text()

                location_el = await element.query_selector("[data-testid='text-location']")
                if location_el:
                    job["location"] = await location_el.inner_text()

                link_el = await element.query_selector("a")
                if link_el:
                    href = await link_el.get_attribute("href")
                    job["url"] = f"{self.BASE_URL}{href}" if href else None

                job["platform"] = "indeed"
                jobs.append(job)
            except Exception as e:
                logger.warning(f"Error parsing Indeed job: {e}")

        return jobs

    def parse_item(self, element: Any) -> Dict[str, Any]:
        return {}
