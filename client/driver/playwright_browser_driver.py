from typing import Any, List, Optional

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

from client.driver.browser_driver import BrowserDriver
from client.utils.headers import get_playwright_extra_headers, get_random_user_agent


class PlaywrightBrowserDriver(BrowserDriver):
    """
    Concrete implementation of BrowserDriver using Playwright.
    Manages Playwright resources properly with context manager support.
    """

    def __init__(self, headless: bool = True, timeout: int = 15000):
        """
        Initialize the Playwright browser driver.

        Args:
            headless: Whether to run browser in headless mode
            timeout: Default timeout in milliseconds
        """
        self._headless = headless
        self._timeout = timeout
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    def __enter__(self):
        """Context manager entry - launches Playwright and browser."""
        self.launch(headless=self._headless)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - properly closes all Playwright resources."""
        self.close()

    def set_timeout(self, timeout: int) -> None:
        """Set the default timeout for page operations."""
        self._timeout = timeout

    def launch(self, headless: bool = True, locale: str = None) -> None:
        """Launch the browser instance with configured settings."""
        if self._playwright is not None:
            raise RuntimeError("Browser already launched. Call close() first.")

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled',
                  '--disable-infobars',
                  '--disable-blink-features',
                  ]
        )
        self._context = self._browser.new_context(
            user_agent=get_random_user_agent(),
            locale='es-ES' if locale is None else locale,
            extra_http_headers=get_playwright_extra_headers()
        )
        self._page = self._context.new_page()

    def close(self) -> None:
        """Close the browser instance and cleanup all resources."""
        try:
            if self._page:
                self._page.close()
                self._page = None
            if self._context:
                self._context.close()
                self._context = None
            if self._browser:
                self._browser.close()
                self._browser = None
        finally:
            if self._playwright:
                self._playwright.stop()
                self._playwright = None

    def new_page(self) -> Page:
        """Open a new browser page/tab."""
        if not self._context:
            raise RuntimeError("Browser not launched. Call launch() or use as context manager.")
        return self._context.new_page()

    def goto(self, url: str, wait_until: Optional[str] = None) -> None:
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
            wait_until: Wait condition ('load', 'domcontentloaded', 'networkidle', 'commit')
        """
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")

        wait_condition = wait_until or "domcontentloaded"
        self._page.goto(url, wait_until=wait_condition)

        # Optionally wait for networkidle if not already specified
        if wait_until != "networkidle":
            try:
                self._page.wait_for_load_state("networkidle", timeout=self._timeout)
            except Exception as e:
                # Non-critical if networkidle fails
                print(f"Warning: networkidle timeout for {url}: {e}")

    def content(self) -> str:
        """Get the full HTML content of the page after rendering."""
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        return self._page.content()

    def query_selector(self, selector: str) -> Optional[Any]:
        """Return the first element matching the selector, or None if not found."""
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        return self._page.query_selector(selector)

    def query_selector_all(self, selector: str) -> List[Any]:
        """Return all elements matching the selector."""
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        elements = self._page.query_selector_all(selector)
        return list(elements) if elements else []

    def inner_text(self, element: Any) -> str:
        """Get the inner text of an element."""
        text = element.inner_text()
        return text if text else ""

    def get_attribute(self, element: Any, attr: str) -> Optional[str]:
        """Get an attribute value from an element, or None if not present."""
        return element.get_attribute(attr)

    def click(self, selector: str) -> None:
        """Click an element matching the selector on the page."""
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.click(selector)

    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Wait for a selector to appear on the page.

        Args:
            selector: CSS selector to wait for
            timeout: Timeout in milliseconds
        """
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.wait_for_selector(selector, timeout=timeout if timeout else self._timeout)

    def evaluate_script(self, script: str) -> Any:
        """
        Execute JavaScript code in the page context.

        Args:
            script: JavaScript code to execute

        Returns:
            The result of the JavaScript execution
        """
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")

        self._page.evaluate(script)

    def click_away(self, x: int, y: int) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.mouse.click(x, y)

    def enter_text(self, selector: str, text: str) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.type(selector, text)

    def press_enter(self, selector: str) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.press(selector, "Enter")

    def arrow_key_down(self, times: int) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        for _ in range(times):
            self._page.keyboard.press("ArrowDown")

    def sroll_to_element(self, selector: str) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.locator(selector).scroll_into_view_if_needed()

    def wait_for_timeout(self, ms: int) -> None:
        if not self._page:
            raise RuntimeError("No page available. Call launch() or use as context manager.")
        self._page.wait_for_timeout(ms)
