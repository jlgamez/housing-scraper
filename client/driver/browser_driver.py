from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BrowserDriver(ABC):
    """
    Abstract interface for browser automation drivers (e.g., Playwright, Selenium).
    Decouples scraping logic from the underlying browser implementation.
    """

    @abstractmethod
    def set_timeout(self, timeout: int) -> None:
        """Set the default timeout for page operations."""
        pass

    @abstractmethod
    def launch(self, headless: bool = True, locale: str = None) -> None:
        """Launch the browser instance."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the browser instance."""
        pass

    @abstractmethod
    def new_page(self) -> Any:
        """Open a new browser page/tab. Returns a page object or handle."""
        pass

    @abstractmethod
    def goto(self, url: str, wait_until: Optional[str] = None) -> None:
        """Navigate to a URL. Optionally wait for a condition (e.g., 'networkidle')."""
        pass

    @abstractmethod
    def content(self) -> str:
        """Get the full HTML content of the page after rendering."""
        pass

    @abstractmethod
    def query_selector(self, selector: str) -> Optional[Any]:
        """Return the first element matching the selector, or None if not found."""
        pass

    @abstractmethod
    def query_selector_all(self, selector: str) -> List[Any]:
        """Return all elements matching the selector."""
        pass

    @abstractmethod
    def inner_text(self, element: Any) -> str:
        """Get the inner text of an element."""
        pass

    @abstractmethod
    def get_attribute(self, element: Any, attr: str) -> Optional[str]:
        """Get an attribute value from an element, or None if not present."""
        pass

    @abstractmethod
    def click(self, selector: str) -> None:
        """Click an element matching the selector on the page."""
        pass

    @abstractmethod
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> None:
        """Wait for a selector to appear on the page (timeout in ms)."""
        pass

    @abstractmethod
    def evaluate_script(self, script: str) -> None:
        """Evaluate a JavaScript script in the context of the page."""
        pass

    @abstractmethod
    def click_away(self, x: int, y: int) -> None:
        """Click at a specific (x, y) coordinate on the page."""
        pass

    @abstractmethod
    def enter_text(self, selector: str, text: str) -> None:
        """Enter text into the currently focused input field."""
        pass

    @abstractmethod
    def press_enter(self, selector: str) -> None:
        """Simulate pressing the Enter key on the focused element."""
        pass

    @abstractmethod
    def arrow_key_down(self, times: int) -> None:
        """Simulate pressing down a key multiple times."""
        pass

    @abstractmethod
    def sroll_to_element(self, selector: str) -> None:
        """Scroll the page to bring the specified element into view."""
        pass

    @abstractmethod
    def wait_for_timeout(self, ms: int) -> None:
        """Wait for the given number of milliseconds."""
        pass
