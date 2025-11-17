"""
Playwright-based scraper with full browser automation
"""
import asyncio
import random
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from loguru import logger
from .base_scraper import BaseScraper


class PlaywrightScraper(BaseScraper):
    """Advanced scraper using Playwright"""

    def __init__(
        self,
        use_proxy: bool = False,
        proxy_list: Optional[List[str]] = None,
        headless: bool = True,
        delay_min: float = 1.0,
        delay_max: float = 3.0,
        browser_type: str = "chromium",  # chromium, firefox, webkit
    ):
        super().__init__(use_proxy, proxy_list, headless, delay_min, delay_max)
        self.browser_type = browser_type
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    async def initialize(self):
        """Initialize Playwright browser"""
        self.playwright = await async_playwright().start()

        # Browser launch arguments for stealth
        launch_args = {
            "headless": self.headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
        }

        # Add proxy if enabled
        if self.use_proxy and self.proxy_list:
            proxy = self.get_random_proxy()
            if proxy:
                self.current_proxy = proxy
                launch_args["proxy"] = {"server": proxy}

        # Launch browser
        if self.browser_type == "firefox":
            self.browser = await self.playwright.firefox.launch(**launch_args)
        elif self.browser_type == "webkit":
            self.browser = await self.playwright.webkit.launch(**launch_args)
        else:
            self.browser = await self.playwright.chromium.launch(**launch_args)

        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=self.get_random_user_agent(),
            locale="en-US",
            timezone_id="America/New_York",
            permissions=["geolocation"],
            geolocation={"latitude": 40.7128, "longitude": -74.0060},
        )

        # Add stealth scripts
        await self.context.add_init_script("""
            // Overwrite the `plugins` property to use a custom getter
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Overwrite the `plugins` property
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Overwrite the `languages` property
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            // Chrome runtime
            window.chrome = {
                runtime: {}
            };
        """)

    async def create_page(self) -> Page:
        """Create new page with anti-detection measures"""
        if not self.context:
            await self.initialize()

        page = await self.context.new_page()

        # Set extra headers
        await page.set_extra_http_headers(self.get_headers())

        return page

    async def scrape(
        self,
        url: str,
        max_pages: int = 1,
        scroll_to_load: bool = False,
        wait_for_selector: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Main scraping method

        Args:
            url: Target URL
            max_pages: Number of pages to scrape
            scroll_to_load: Whether to scroll to load dynamic content
            wait_for_selector: CSS selector to wait for before scraping
        """
        results = []

        try:
            page = await self.create_page()

            for page_num in range(1, max_pages + 1):
                logger.info(f"Scraping page {page_num} of {max_pages}: {url}")

                # Navigate to URL
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                except Exception as e:
                    logger.error(f"Error navigating to {url}: {e}")
                    continue

                # Wait for specific selector if provided
                if wait_for_selector:
                    try:
                        await page.wait_for_selector(wait_for_selector, timeout=10000)
                    except Exception as e:
                        logger.warning(f"Selector {wait_for_selector} not found: {e}")

                # Scroll if needed
                if scroll_to_load:
                    await self.scroll_page(page)

                # Random delay
                self.random_delay()

                # Check for captcha
                if await self.detect_captcha(page):
                    logger.warning("Captcha detected!")
                    await self.handle_captcha(page)

                # Extract data
                page_results = await self.extract_data(page)
                results.extend(page_results)

                # Get next page URL
                next_url = await self.get_next_page_url(page)
                if not next_url or page_num >= max_pages:
                    break

                url = next_url

            await page.close()

        except Exception as e:
            logger.error(f"Scraping error: {e}", exc_info=True)

        return results

    async def extract_data(self, page: Page) -> List[Dict[str, Any]]:
        """Extract data from page - to be overridden by subclasses"""
        # This is a default implementation
        items = []

        # Example: extract all article elements
        elements = await page.query_selector_all("article, .job-listing, .opportunity")

        for element in elements:
            try:
                item = await self.parse_item_async(element)
                if item:
                    items.append(item)
            except Exception as e:
                logger.warning(f"Error parsing item: {e}")

        return items

    async def parse_item_async(self, element: Any) -> Dict[str, Any]:
        """Parse single item asynchronously"""
        # Override in subclass
        return {}

    def parse_item(self, element: Any) -> Dict[str, Any]:
        """Parse single item - sync version for compatibility"""
        return {}

    async def detect_captcha(self, page: Page) -> bool:
        """Detect if captcha is present"""
        captcha_selectors = [
            "iframe[src*='recaptcha']",
            "iframe[src*='hcaptcha']",
            ".g-recaptcha",
            "#captcha",
            "[data-sitekey]",
        ]

        for selector in captcha_selectors:
            element = await page.query_selector(selector)
            if element:
                return True

        return False

    async def get_next_page_url(self, page: Page) -> Optional[str]:
        """Get next page URL from pagination"""
        next_selectors = [
            "a.next",
            "a[rel='next']",
            "button.next",
            ".pagination .next",
            "[aria-label='Next']",
        ]

        for selector in next_selectors:
            element = await page.query_selector(selector)
            if element:
                href = await element.get_attribute("href")
                if href:
                    # Handle relative URLs
                    if href.startswith("/"):
                        current_url = page.url
                        base_url = "/".join(current_url.split("/")[:3])
                        return base_url + href
                    return href

        return None

    async def login(self, page: Page, username: str, password: str, login_url: str):
        """Generic login method"""
        await page.goto(login_url)
        await page.wait_for_load_state("networkidle")

        # Common username/email field selectors
        username_selectors = [
            "input[type='email']",
            "input[name='username']",
            "input[name='email']",
            "#username",
            "#email",
        ]

        for selector in username_selectors:
            element = await page.query_selector(selector)
            if element:
                await element.fill(username)
                break

        # Common password field selectors
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "#password",
        ]

        for selector in password_selectors:
            element = await page.query_selector(selector)
            if element:
                await element.fill(password)
                break

        # Submit
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Sign in')",
            "button:has-text('Log in')",
        ]

        for selector in submit_selectors:
            element = await page.query_selector(selector)
            if element:
                await element.click()
                break

        await page.wait_for_load_state("networkidle")

    async def close(self):
        """Close browser and cleanup"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
