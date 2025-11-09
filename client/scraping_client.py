from abc import ABC, abstractmethod
from typing import Optional


class ScraperClient(ABC):

    @abstractmethod
    def visit_page(self, url: str):
        """Visit a web page and return its content as a string."""
        pass

    @abstractmethod
    def deflect_popups(self):
        """Deflect pop-ups or modals if any appear."""
        pass

    @abstractmethod
    def wait_for_element(self, selector: str, timeout: int):
        """Wait for a specific element to appear on the page."""
        pass

    @abstractmethod
    def get_page_content(self) -> Optional[str]:
        """Retrieve the current page content as a string."""
        pass

    @abstractmethod
    def next_page(self) -> bool:
        """Navigate to the next page if available."""
        pass

    @abstractmethod
    def vertical_scroll_to(self, js_string_position: str):
        """Scroll to a specific position on the page."""
        pass

    @abstractmethod
    def scroll_to_element(self, element_locator: str):
        """Scroll to an element identified by a JavaScript string."""
        pass

    @abstractmethod
    def press_button(self, button_locator: str):
        """Press a button identified by a JavaScript string."""
        pass

    @abstractmethod
    def search_select(self, field_locator: str, value: str, option_number: int):
        """Fill an input field identified by a JavaScript string with a given value and select the option number."""
        pass
