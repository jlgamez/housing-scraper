import logging
import random
from time import sleep
from typing import Optional

from client.driver.browser_driver import BrowserDriver
from client.scraping_client import ScraperClient
from client.site.site_strategy import SiteStrategy

DEFAULT_TIMEOUT = 15000
VERTICAL_SCROLL_JS = 'window.scrollTo(0, Y_COORDINATE)'


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
        sleep(random.uniform(0.5, 2.0))
        self._driver.arrow_key_down(option_number)
        sleep(random.uniform(0.5, 2.0))
        self._driver.press_enter(search_field_locator)

    def scroll_to_element(self, element_locator: str):
        self._site_strategy.scroll_to_element(element_locator)
