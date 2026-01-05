import logging
import random
from time import sleep

from client.driver.browser_driver import BrowserDriver
from client.site.site_strategy import SiteStrategy
from common.locators.foto_casa_selectors import FOTO_CASA_ACCEPT_COOKIES_BUTTON, \
    FOTO_CASA_SUBSCRIPTION_MODAL, FOTO_CASA_NEXT_PAGE_BUTTON, FOTO_CASA_ALERT_BUTTON


class FotoCasaStrategy(SiteStrategy):

    def __init__(self, listings_first_url: str):
        self._driver: BrowserDriver = None  # type: ignore
        self.listings_url = listings_first_url
        self._page_number = 1
        self.pagination_blocked = False

    def set_driver(self, driver: BrowserDriver):
        self._driver = driver

    def deflect_popups(self) -> bool:
        if not self._driver:
            raise RuntimeError("Driver not set. Call set_driver() before deflecting popups.")

        try:  # Accept cookies if the button is present
            self._driver.wait_for_selector(FOTO_CASA_ACCEPT_COOKIES_BUTTON)

            if self._driver.query_selector(FOTO_CASA_ACCEPT_COOKIES_BUTTON):
                sleep(random.uniform(0.2, 0.5))
                self._driver.click(FOTO_CASA_ACCEPT_COOKIES_BUTTON)
                sleep(random.uniform(0.2, 0.5))
        except Exception as e:
            logging.info("Cookies modal not found " + str(e))

        try:  # Deflect subscription modal if present
            self._driver.wait_for_selector(FOTO_CASA_SUBSCRIPTION_MODAL)

            if self._driver.query_selector(FOTO_CASA_SUBSCRIPTION_MODAL):
                sleep(random.uniform(0.2, 0.5))
                self._driver.click_away(100, 100)
                sleep(random.uniform(0.2, 0.5))
        except Exception as e:
            logging.info("subscription modal not found " + str(e))

        return self._driver.query_selector(FOTO_CASA_SUBSCRIPTION_MODAL) is None and self._driver.query_selector(
            FOTO_CASA_ACCEPT_COOKIES_BUTTON) is None

    def next_page(self) -> bool:
        if not self._driver:
            raise RuntimeError("Driver not set. Call set_driver() before navigating to next page.")

        self.paginate_manually()

    def update_listings_url(self):
        """
        Update the listings URL to navigate to the next page.
        """
        # Check if URL already has a page number
        if self.listings_url.endswith('/l'):
            # First time - append page 2
            self._page_number = 2
            self.listings_url = f"{self.listings_url}/{self._page_number}"
        else:
            # URL already has a page number, increment it
            self._page_number += 1
            # Replace the last number in the URL with the new page number
            url_parts = self.listings_url.rsplit('/', 1)
            self.listings_url = f"{url_parts[0]}/{self._page_number}"

    def is_pagination_blocked(self):
        try:
            self._driver.wait_for_selector(FOTO_CASA_ALERT_BUTTON, timeout=2000)
            return False
        except Exception as e:
            logging.info("No pagination alert found " + str(e))
            return True

    def paginate_manually(self):
        """
        Paginate by clicking the "Next Page" button.
        """
        if not self._driver:
            raise RuntimeError("Driver not set. Call set_driver() before paginating manually.")

        self.scroll_to_element(FOTO_CASA_NEXT_PAGE_BUTTON)
        self._driver.wait_for_selector(FOTO_CASA_NEXT_PAGE_BUTTON)
        self._driver.click(FOTO_CASA_NEXT_PAGE_BUTTON)

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll to a lazy-loaded element by scrolling gradually to trigger lazy loading.

        Args:
            selector: CSS selector of the element
        """

        if not self._driver:
            raise RuntimeError("Driver not set. Call set_driver() before scrolling to element.")

        # Scroll gradually until element appears
        while not self._driver.query_selector(selector):
            # Scroll down by viewport height
            self._driver.evaluate_script("window.scrollBy(0, window.innerHeight)")
            self._driver.wait_for_timeout(
                int(random.uniform(600, 800)))  # wait for random number of ms (200 - 400) to allow loading

        # Once found, scroll directly to it
        self._driver.scroll_to_element(selector)

    def get_total_pages(self) -> int:

        pass
