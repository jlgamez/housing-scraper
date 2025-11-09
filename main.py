import logging

from client.driver.browser_driver import BrowserDriver
from client.driver.factory import get_browser_driver
from client.scraping_client import ScraperClient
from client.scraping_client_impl import ScrapingClientImpl
from client.site.foto_casa_strategy import FotoCasaStrategy
from client.utils.headers import get_spain_locale
from common.selectors.foto_casa_selectors import FOTO_CASA_SEARCH_BAR

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

FOTO_CASA_ENTRY_URL = 'https://www.fotocasa.es/es/'
FOTO_CASA_LISTINGS_FIRST_URL = 'https://www.fotocasa.es/es/comprar/viviendas/barcelona-capital/sant-marti/l'

if __name__ == '__main__':
    html = None
    driver: BrowserDriver = get_browser_driver()
    foto_casa_strategy = FotoCasaStrategy(listings_first_url=FOTO_CASA_LISTINGS_FIRST_URL)

    # configure scraping client
    scraper_client: ScraperClient = (ScrapingClientImpl.Builder()
                                     .with_driver(driver=driver)
                                     .with_site_strategy(site_strategy=foto_casa_strategy)
                                     .with_locale(locale=get_spain_locale())
                                     .with_headless(headless=False)
                                     .with_timeout(timeout=2000)
                                     .build())

    try:
        with  scraper_client as foto_casa:
            foto_casa.visit_page(FOTO_CASA_ENTRY_URL)
            foto_casa.deflect_popups()

            logging.debug('performing human behaviour')
            foto_casa.perform_random_human_action()
            foto_casa.human_wait()

            # search neighbourhood
            logging.info('search bar inputting...')
            foto_casa.search_select(FOTO_CASA_SEARCH_BAR, 'Sant Martí, Barcelona Capital', 1)
            foto_casa.human_wait()
            foto_casa.deflect_popups()
            foto_casa.human_wait()

            # --- listings info extraction ----

            pages = foto_casa.extract_number_of_pages()

            for page_number in range(1, pages):
                logging.debug(f'performing pagination to number {page_number}')
                foto_casa.next_page()
                foto_casa.human_wait()
                foto_casa.perform_random_human_action()

    except Exception as exception:
        logging.error(f"Exception obtaining page: {exception}")
    finally:
        SystemExit()
