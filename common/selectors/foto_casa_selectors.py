"""
Centralized CSS selectors for Fotocasa listing card parsing.

Update these selectors after inspecting the actual HTML structure of Fotocasa result pages.

Pattern: one constant per field, grouped by context (listing card, fields, features).
"""
LISTING_CARD = 'article.\\@container.w-full'  # Top-level card element (placeholder)

# --- Per-card fields ---
PRICE = '.listing-card-price'  # Price field (placeholder)
ADDRESS = 'h3 a span'  # Address/location field (placeholder)
SIZE = '.listing-card-size'  # Size field (placeholder)
BATHROOMS = '.listing-card-bathrooms'  # Bathrooms field (placeholder)
FLOOR = '.listing-card-floor'  # Floor field (placeholder)

# --- Features/flags ---
ELEVATOR = '.icon-elevator, [alt*=\'ascensor\'], [title*=\'ascensor\']'  # Elevator icon/text (placeholder)

# --- Other useful selectors ---
LISTING_URL = 'a.listing-card-link'  # Link to detail page (for deduplication)

# -- Pagination ---
FOTO_CASA_NO_RESULTS_MESSAGE = '.re-SearchNoResults'  # No results message (placeholder)

# Popups/modals
FOTO_CASA_ACCEPT_COOKIES_BUTTON = '#didomi-notice-agree-button'
FOTO_CASA_SUBSCRIPTION_MODAL = '//*[@id="modal-react-portal"]/div/div'

# fields/actions
FOTO_CASA_SEARCH_BAR = '//*[@id="main-content"]/div/div/div/div[1]/div[2]/div/form/div[1]/div/div/div/div/input'
FOTO_CASA_NEXT_PAGE_BUTTON = '//*[contains(@id, "pagination") and contains(@id, "next")]'
