"""
Upwork job scraper
"""
from typing import Dict, List, Any, Optional
from loguru import logger
from .playwright_scraper import PlaywrightScraper


class UpworkScraper(PlaywrightScraper):
    """Scraper for Upwork freelance jobs"""

    BASE_URL = "https://www.upwork.com"
    SEARCH_URL = "https://www.upwork.com/nx/search/jobs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def scrape_jobs(
        self,
        keywords: str = "",
        category: Optional[str] = None,
        max_pages: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Scrape Upwork jobs

        Args:
            keywords: Search keywords
            category: Job category
            max_pages: Number of pages to scrape
            filters: Additional filters (budget, experience_level, etc.)
        """
        # Build search URL
        search_params = []
        if keywords:
            search_params.append(f"q={keywords.replace(' ', '+')}")
        if category:
            search_params.append(f"category2_uid={category}")

        if filters:
            if filters.get("budget_min"):
                search_params.append(f"amount_min={filters['budget_min']}")
            if filters.get("budget_max"):
                search_params.append(f"amount_max={filters['budget_max']}")
            if filters.get("experience_level"):
                search_params.append(f"experience_level={filters['experience_level']}")

        search_url = f"{self.SEARCH_URL}?{'&'.join(search_params)}"

        logger.info(f"Scraping Upwork jobs: {search_url}")

        return await self.scrape(
            url=search_url,
            max_pages=max_pages,
            scroll_to_load=True,
            wait_for_selector="article[data-test='job-tile']",
        )

    async def extract_data(self, page) -> List[Dict[str, Any]]:
        """Extract job listings from Upwork page"""
        jobs = []

        # Wait for job tiles to load
        await page.wait_for_selector("article[data-test='job-tile']", timeout=10000)

        # Get all job tiles
        job_elements = await page.query_selector_all("article[data-test='job-tile']")

        logger.info(f"Found {len(job_elements)} job listings")

        for element in job_elements:
            try:
                job = await self.parse_upwork_job(element, page)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"Error parsing job: {e}")

        return jobs

    async def parse_upwork_job(self, element, page) -> Dict[str, Any]:
        """Parse single Upwork job"""
        job = {}

        try:
            # Title and URL
            title_element = await element.query_selector("h2.job-tile-title a")
            if title_element:
                job["title"] = await title_element.inner_text()
                href = await title_element.get_attribute("href")
                job["url"] = f"{self.BASE_URL}{href}" if href else None

            # Description
            desc_element = await element.query_selector("[data-test='job-description']")
            if desc_element:
                job["description"] = await desc_element.inner_text()

            # Budget
            budget_element = await element.query_selector("[data-test='budget']")
            if budget_element:
                budget_text = await budget_element.inner_text()
                job["budget"] = self.parse_budget(budget_text)

            # Job type (Fixed/Hourly)
            job_type_element = await element.query_selector("[data-test='job-type-label']")
            if job_type_element:
                job_type = await job_type_element.inner_text()
                job["is_fixed_price"] = "fixed" in job_type.lower()

            # Skills
            skill_elements = await element.query_selector_all("[data-test='token-skill']")
            job["skills"] = []
            for skill_el in skill_elements:
                skill_text = await skill_el.inner_text()
                job["skills"].append(skill_text.strip())

            # Experience level
            exp_element = await element.query_selector("[data-test='experience-level']")
            if exp_element:
                job["experience_level"] = await exp_element.inner_text()

            # Posted time
            posted_element = await element.query_selector("[data-test='posted-on']")
            if posted_element:
                job["posted_on"] = await posted_element.inner_text()

            # Client info
            client_element = await element.query_selector("[data-test='client-info']")
            if client_element:
                client_text = await client_element.inner_text()
                job["client_info"] = client_text

            # Payment verified
            verified_element = await element.query_selector("[data-test='payment-verified']")
            job["payment_verified"] = verified_element is not None

            # Platform
            job["platform"] = "upwork"
            job["source"] = "upwork"

        except Exception as e:
            logger.error(f"Error parsing Upwork job details: {e}")

        return job

    def parse_budget(self, budget_text: str) -> Dict[str, Any]:
        """Parse budget string"""
        budget_info = {
            "min": None,
            "max": None,
            "currency": "USD",
            "rate_type": "fixed",
        }

        try:
            # Remove currency symbols and clean
            clean_text = budget_text.replace("$", "").replace(",", "").strip()

            # Check if it's hourly
            if "hr" in clean_text.lower() or "hour" in clean_text.lower():
                budget_info["rate_type"] = "hourly"

            # Extract numbers
            import re
            numbers = re.findall(r"\d+(?:\.\d+)?", clean_text)

            if len(numbers) == 2:
                budget_info["min"] = float(numbers[0])
                budget_info["max"] = float(numbers[1])
            elif len(numbers) == 1:
                budget_info["min"] = float(numbers[0])
                budget_info["max"] = float(numbers[0])

        except Exception as e:
            logger.warning(f"Error parsing budget: {e}")

        return budget_info

    def parse_item(self, element: Any) -> Dict[str, Any]:
        """Sync version - not used with Playwright"""
        return {}
