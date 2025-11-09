from abc import ABC, abstractmethod

from client.driver.browser_driver import BrowserDriver


class SiteStrategy(ABC):

    @abstractmethod
    def set_driver(self, driver: BrowserDriver):
        """Set the browser driver for the strategy."""
        pass

    @abstractmethod
    def deflect_popups(self) -> bool:
        """Deflect pop-ups or modals if any appear."""
        pass

    @abstractmethod
    def next_page(self) -> bool:
        """Navigate to the next page if available."""
        pass

    @abstractmethod
    def scroll_to_element(self, selector: str) -> None:
        """Scroll to an element identified by a selector."""
        pass

    @abstractmethod
    def get_total_pages(self) -> int:
        """Get the total number of pages available."""
        pass
