import random
from typing import Optional, List

# Realistic, diverse user-agents (desktop and mobile)
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
]

_ACCEPTS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
]

_ACCEPT_LANGUAGES = [
    "es-ES,es;q=0.9",
    "es-ES,es;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7",
]

_PLAYWRIGHT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

_PLAYWRIGHT_EXTRA_HEADERS = {
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate"
}

_SPAIN_LOCALE = "es-ES"


def get_spain_locale() -> str:
    """Return the locale string for Spain."""
    return _SPAIN_LOCALE


def get_playwright_user_agent() -> str:
    """Return the fixed User-Agent string used by PlaywrightClient."""
    return _PLAYWRIGHT_USER_AGENT


def get_playwright_extra_headers() -> dict:
    """Return a copy of the extra headers used by PlaywrightClient."""
    return _PLAYWRIGHT_EXTRA_HEADERS.copy()


def get_user_agents() -> List[str]:
    """Return a copy of the configured user agent list."""
    return _USER_AGENTS.copy()


def get_random_user_agent() -> str:
    """Return a random User-Agent string."""
    return random.choice(_USER_AGENTS)


def get_accepts() -> List[str]:
    """Return a copy of the Accept header options."""
    return _ACCEPTS.copy()


def get_random_accept() -> str:
    """Return a random Accept header value."""
    return random.choice(_ACCEPTS)


def get_accept_languages() -> List[str]:
    """Return a copy of Accept-Language options."""
    return _ACCEPT_LANGUAGES.copy()


def get_random_accept_language() -> str:
    """Return a random Accept-Language value."""
    return random.choice(_ACCEPT_LANGUAGES)


def get_headers(referer: Optional[str] = None) -> dict:
    """
    Build randomized, coherent request headers for navigation requests.
    """
    user_agent = random.choice(_USER_AGENTS)
    headers = {
        "User-Agent": user_agent,
        "Accept": random.choice(_ACCEPTS),
        "Accept-Language": random.choice(_ACCEPT_LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.idealista.com/"
    }
    if referer:
        headers["Referer"] = referer
    return headers
