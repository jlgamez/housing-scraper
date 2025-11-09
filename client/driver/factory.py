from client.driver.browser_driver import BrowserDriver
from client.driver.playwright_browser_driver import PlaywrightBrowserDriver


def get_browser_driver() -> BrowserDriver:
    return PlaywrightBrowserDriver()
