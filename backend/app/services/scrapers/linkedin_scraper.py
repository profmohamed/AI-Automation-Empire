"""
LinkedIn job scraper
"""
from typing import Dict, List, Any, Optional
from loguru import logger
from .playwright_scraper import PlaywrightScraper


class LinkedInScraper(PlaywrightScraper):
    """Scraper for LinkedIn jobs"""

    BASE_URL = "https://www.linkedin.com"
    JOBS_URL = "https://www.linkedin.com/jobs/search"

    async def scrape_jobs(
        self,
        keywords: str = "",
        location: str = "",
        max_pages: int = 5,
        job_type: Optional[str] = None,  # full-time, part-time, contract, etc.
        experience_level: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Scrape LinkedIn jobs"""
        params = []
        if keywords:
            params.append(f"keywords={keywords.replace(' ', '%20')}")
        if location:
            params.append(f"location={location.replace(' ', '%20')}")
        if job_type:
            params.append(f"f_JT={job_type}")
        if experience_level:
            params.append(f"f_E={experience_level}")

        search_url = f"{self.JOBS_URL}?{'&'.join(params)}"
        logger.info(f"Scraping LinkedIn jobs: {search_url}")

        return await self.scrape(
            url=search_url,
            max_pages=max_pages,
            scroll_to_load=True,
            wait_for_selector=".jobs-search__results-list",
        )

    async def extract_data(self, page) -> List[Dict[str, Any]]:
        """Extract job listings from LinkedIn"""
        jobs = []

        try:
            await page.wait_for_selector(".jobs-search__results-list", timeout=10000)

            # Scroll to load all jobs
            await self.scroll_page(page, scroll_count=3)

            # Get all job cards
            job_elements = await page.query_selector_all(".base-card")

            logger.info(f"Found {len(job_elements)} LinkedIn jobs")

            for element in job_elements:
                try:
                    job = await self.parse_linkedin_job(element, page)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"Error parsing LinkedIn job: {e}")

        except Exception as e:
            logger.error(f"Error extracting LinkedIn jobs: {e}")

        return jobs

    async def parse_linkedin_job(self, element, page) -> Dict[str, Any]:
        """Parse single LinkedIn job"""
        job = {}

        try:
            # Title
            title_element = await element.query_selector(".base-search-card__title")
            if title_element:
                job["title"] = await title_element.inner_text()

            # Company
            company_element = await element.query_selector(".base-search-card__subtitle")
            if company_element:
                job["company"] = await company_element.inner_text()

            # Location
            location_element = await element.query_selector(".job-search-card__location")
            if location_element:
                job["location"] = await location_element.inner_text()

            # URL
            link_element = await element.query_selector("a.base-card__full-link")
            if link_element:
                href = await link_element.get_attribute("href")
                job["url"] = href

            # Posted date
            date_element = await element.query_selector("time")
            if date_element:
                job["posted_date"] = await date_element.get_attribute("datetime")

            job["platform"] = "linkedin"
            job["source"] = "linkedin"

        except Exception as e:
            logger.error(f"Error parsing LinkedIn job: {e}")

        return job

    def parse_item(self, element: Any) -> Dict[str, Any]:
        """Sync version"""
        return {}
