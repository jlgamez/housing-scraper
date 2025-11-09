import logging
import random

from client.driver.browser_driver import BrowserDriver
from client.driver.factory import get_browser_driver
from client.scraping_client import ScraperClient
from client.scraping_client_impl import ScrapingClientImpl
from client.site.foto_casa_strategy import FotoCasaStrategy
from client.utils.browser_actions import random_sleep
from client.utils.headers import get_spain_locale
from common.selectors.foto_casa_selectors import FOTO_CASA_SEARCH_BAR, FOTO_CASA_NEXT_PAGE_BUTTON

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

FOTO_CASA_ENTRY_URL = 'https://www.fotocasa.es/es/'

if __name__ == '__main__':
    html = None
    driver: BrowserDriver = get_browser_driver()
    foto_casa_strategy = FotoCasaStrategy(initial_url=FOTO_CASA_ENTRY_URL)

    scraper_client: ScraperClient = (ScrapingClientImpl.Builder()
                                     .with_driver(driver=driver)
                                     .with_site_strategy(site_strategy=foto_casa_strategy)
                                     .with_locale(locale=get_spain_locale())
                                     .with_headless(headless=False)
                                     .with_timeout(timeout=2000)
                                     .build())

    # configure scraping client
    with  scraper_client as foto_casa:
        try:
            foto_casa.visit_page(FOTO_CASA_ENTRY_URL)
            foto_casa.deflect_popups()
            logging.info('popups deflected successfully. Attempting pagination...')

            logging.debug('performing human behaviour')
            random_sleep()
            foto_casa.vertical_scroll_to(str(random.randint(300, 1200)))
            random_sleep()
            foto_casa.vertical_scroll_to(str(0))
            random_sleep()

            # search neighbourhood
            logging.info('search bar inputting...')
            foto_casa.search_select(FOTO_CASA_SEARCH_BAR, 'Sant Martí, Barcelona Capital', 1)
            random_sleep()
            foto_casa.deflect_popups()

            # random scrolling
            logging.debug('random scrolling')
            foto_casa.vertical_scroll_to(str(random.randint(500, 3200)))
            random_sleep()
            foto_casa.vertical_scroll_to(str(0))

            # paginate
            random_sleep()
            foto_casa.scroll_to_element(FOTO_CASA_NEXT_PAGE_BUTTON)
            random_sleep()
            foto_casa.next_page()
            random_sleep()

        except Exception as exception:
            logging.error(f"Exception obtaining page: {exception}")
        finally:
            SystemExit()
