import logging
import random
from time import sleep

from client.driver.browser_driver import BrowserDriver
from client.site.site_strategy import SiteStrategy
from common.selectors.foto_casa_selectors import FOTO_CASA_ACCEPT_COOKIES_BUTTON, \
    FOTO_CASA_SUBSCRIPTION_MODAL, FOTO_CASA_NEXT_PAGE_BUTTON


class FotoCasaStrategy(SiteStrategy):

    def __init__(self, initial_url: str):
        self._driver: BrowserDriver = None  # type: ignore
        self._url = initial_url
        self._page_number = 1

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
        try:
            self._driver.wait_for_selector(FOTO_CASA_NEXT_PAGE_BUTTON)
            self._driver.click(FOTO_CASA_NEXT_PAGE_BUTTON)
        except Exception as e:
            logging.error(e)
            return False

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
        self._driver.sroll_to_element(selector)
