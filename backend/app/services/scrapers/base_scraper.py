"""
Base scraper with anti-bot features
"""
import random
import time
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from loguru import logger
from fake_useragent import UserAgent
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseScraper(ABC):
    """Base scraper class with anti-bot protection"""

    def __init__(
        self,
        use_proxy: bool = False,
        proxy_list: Optional[List[str]] = None,
        headless: bool = True,
        delay_min: float = 1.0,
        delay_max: float = 3.0,
    ):
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.headless = headless
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.ua = UserAgent()
        self.session = None
        self.current_proxy = None

    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        return self.ua.random

    def get_random_proxy(self) -> Optional[str]:
        """Get random proxy from list"""
        if not self.proxy_list:
            return None
        return random.choice(self.proxy_list)

    def random_delay(self):
        """Random delay to avoid detection"""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)

    def get_headers(self) -> Dict[str, str]:
        """Get realistic headers"""
        return {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_page(self, url: str) -> str:
        """Fetch page with retry logic"""
        headers = self.get_headers()
        proxy = self.get_random_proxy() if self.use_proxy else None

        async with httpx.AsyncClient(proxies=proxy, timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            self.random_delay()
            return response.text

    def extract_text(self, element: Any, selector: str, default: str = "") -> str:
        """Extract text from element"""
        try:
            if hasattr(element, 'query_selector'):
                el = element.query_selector(selector)
                return el.inner_text() if el else default
            return default
        except Exception as e:
            logger.warning(f"Error extracting text: {e}")
            return default

    def extract_attribute(
        self, element: Any, selector: str, attribute: str, default: str = ""
    ) -> str:
        """Extract attribute from element"""
        try:
            if hasattr(element, 'query_selector'):
                el = element.query_selector(selector)
                return el.get_attribute(attribute) if el else default
            return default
        except Exception as e:
            logger.warning(f"Error extracting attribute: {e}")
            return default

    @abstractmethod
    async def scrape(self, **kwargs) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by subclasses"""
        pass

    @abstractmethod
    def parse_item(self, element: Any) -> Dict[str, Any]:
        """Parse single item from page"""
        pass

    async def scroll_page(self, page: Any, scroll_count: int = 5):
        """Scroll page to load dynamic content"""
        for _ in range(scroll_count):
            await page.evaluate("window.scrollBy(0, window.innerHeight)")
            await page.wait_for_timeout(random.randint(1000, 2000))

    async def handle_captcha(self, page: Any) -> bool:
        """Handle captcha if detected"""
        # This is a placeholder - implement with 2captcha or similar
        logger.warning("Captcha detected! Manual intervention or solver required.")
        return False

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        return " ".join(text.split()).strip()

    async def close(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
