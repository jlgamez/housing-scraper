import logging
import random
from enum import Enum
from typing import Optional

from client.driver.browser_driver import BrowserDriver
from client.scraping_client import ScraperClient
from client.site.site_strategy import SiteStrategy
from client.utils.browser_actions import random_driver_sleep, random_mouse_movement, random_scroll
from common.selectors.foto_casa_selectors import FOTO_CASA_PAGES_NUMBER

DEFAULT_TIMEOUT = 15000
VERTICAL_SCROLL_JS = 'window.scrollTo(0, Y_COORDINATE)'


class HumanAction(Enum):
    SCROLL = 'scroll'
    MOUSE_MOVE = 'mouse_move'
    WAIT = 'wait'


class ScrapingClientImpl(ScraperClient):

    def __init__(
            self,
            driver: BrowserDriver,
            site_strategy: SiteStrategy,
            timeout: int,
            is_headless: bool = True
    ):
        self._driver = driver
        self._site_strategy = site_strategy
        self._driver.set_timeout(timeout if timeout else DEFAULT_TIMEOUT)

        self._site_strategy.set_driver(self._driver)
        self._is_driver_ready = False
        self._is_headless = is_headless

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver:
            self._driver.close()

    class Builder:
        def __init__(self):
            self._site_strategy = None
            self._timeout = None
            self._driver: BrowserDriver = None
            self._locale: str = None
            self._is_headless: bool = True

        def with_driver(self, driver: BrowserDriver):
            self._driver = driver
            return self

        def with_site_strategy(self, site_strategy: SiteStrategy):
            self._site_strategy = site_strategy
            return self

        def with_headless(self, headless: bool):
            self._is_headless = headless
            return self

        def with_timeout(self, timeout: int):
            self._timeout = timeout
            return self

        def with_locale(self, locale: str):
            self._locale = locale
            return self

        def build(self) -> ScraperClient:
            if not self._driver:
                raise ValueError("BrowserDriver must be provided to build ScrapingClientImpl.")

            if not self._site_strategy:
                raise ValueError("SiteStrategy must be provided to build ScrapingClientImpl.")

            return ScrapingClientImpl(
                driver=self._driver,
                site_strategy=self._site_strategy,
                is_headless=self._is_headless,
                timeout=self._timeout
            )

    def visit_page(self, url: str):
        if not self._is_driver_ready:
            self.initialise_driver()

        self._driver.goto(url)

    def deflect_popups(self):
        self._site_strategy.deflect_popups()

    def wait_for_element(self, selector: str, timeout: int):
        if not self._is_driver_ready:
            self.initialise_driver()
        self._driver.wait_for_selector(selector, timeout)

    def get_page_content(self) -> Optional[str]:
        return self._driver.content()

    def next_page(self) -> bool:
        return self._site_strategy.next_page()

    def vertical_scroll_to(self, js_string_position: str):
        js_code = VERTICAL_SCROLL_JS.replace("Y_COORDINATE", js_string_position)
        self._driver.evaluate_script(js_code)

    def initialise_driver(self):
        if not self._driver:
            raise RuntimeError("BrowserDriver is not set.")

        # launch the driver
        self._driver.launch(headless=self._is_headless)
        self._is_driver_ready = True
        logging.info("BrowserDriver launched with headless=%s", self._is_headless)

    def press_button(self, button_locator: str):
        self._driver.click(selector=button_locator)

    def search_select(self, search_field_locator: str, value: str, option_number: int):
        self._driver.enter_text(search_field_locator, value)
        self.human_wait()
        self._driver.arrow_key_down(option_number)
        self.human_wait(micro_wait=True)
        self._driver.press_enter(search_field_locator)

    def scroll_to_element(self, element_locator: str):
        self._site_strategy.scroll_to_element(element_locator)

    def human_wait(self, micro_wait: bool = False):
        random_driver_sleep(self._driver, micro_wait=micro_wait)

    def random_scroll(self):
        """
        Simulate random scrolling behavior and return to original position.
        This helps mimic human browsing patterns to avoid bot detection.
        """
        if not self._driver:
            raise RuntimeError("BrowserDriver is not set.")

        random_scroll(self._driver)

    def random_mouse_move(self):
        """
        Simulate random mouse movements on the page.
        """
        if not self._driver:
            raise RuntimeError("BrowserDriver is not set.")
        random_mouse_movement(self._driver)

    def perform_random_human_action(self):
        # choose a random action to perform
        action = random.choice(list(HumanAction))
        # perform the action using /client/utils/browser_actions.py functions
        if action == HumanAction.SCROLL:
            self.random_scroll()
        elif action == HumanAction.MOUSE_MOVE:
            self.random_mouse_move()
        elif action == HumanAction.WAIT:
            self.human_wait()

    def extract_number_of_pages(self) -> int:
        self._site_strategy.scroll_to_element(FOTO_CASA_PAGES_NUMBER)
        number_of_pages = self._driver.query_selector(FOTO_CASA_PAGES_NUMBER).text_content()
        if number_of_pages:
            return int(number_of_pages)
        return 1
