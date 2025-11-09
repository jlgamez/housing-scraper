"""
Parser scaffold for Fotocasa listings result pages.

Scope: given the HTML of a search results page (list of property cards),
extract for each card:
- address
- price (EUR, numeric)
- size (m2, numeric)
- number of bathrooms (numeric)
- floor number (numeric when available; e.g., 3 for "3ª planta").

This is only a scaffold: all functions are defined with clear contracts but
intentionally unimplemented (raise NotImplementedError).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from common.selectors.foto_casa_selectors import LISTING_CARD, ADDRESS


# -----------------------------
# Data model
# -----------------------------
@dataclass
class ListingSummary:
    """Lightweight, parsed data for a single listing card.
    Fields are Optional when the attribute might be missing on the card.
    """
    address: Optional[str]
    price_eur: Optional[int]
    size_m2: Optional[int]
    bathrooms: Optional[int]
    floor_number: Optional[int]


# -----------------------------
# Public, high-level API
# -----------------------------
def parse_listings_page(html: str) -> List[ListingSummary]:
    """Parse a Fotocasa search results page HTML into listing summaries.

    Inputs:
      - html: Full HTML text of a search/listing results page.

    Output:
      - List of ListingSummary parsed from the visible listing cards in the page.

    Notes:
      - This function should not follow links into detail pages.
      - Pagination is out of scope here (handled by the caller).
    """
    cards = extract_listing_cards(html)
    return [parse_listing_card(single_card) for single_card in cards]


# -----------------------------
# Card discovery
# -----------------------------
def extract_listing_cards(html: str) -> List[Tag]:
    """Locate and yield each listing card element from the page HTML.

    Returns a list of BeautifulSoup Tag objects representing listing cards.
    Uses the centralized LISTING_CARD selector from foto_casa_selectors.py.
    Replace the placeholder selector with the actual Fotocasa card selector after inspecting HTML.
    """
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(LISTING_CARD)
    return cards


# -----------------------------
# Per-card parsing
# -----------------------------
def parse_listing_card(card: Tag) -> ListingSummary:
    """Parse a single listing card into a ListingSummary.

    The input `card` is a parsed HTML element (bs4.element.Tag).
    This function composes the atomic field parsers below.
    """
    return ListingSummary(
        address=parse_address(card),
        price_eur=parse_price(card),
        size_m2=parse_size(card),
        bathrooms=parse_bathrooms(card),
        floor_number=parse_floor_number(card),
    )


def parse_address(card: Tag) -> Optional[str]:
    """Extract the short address/location string from a listing card.
    Returns cleaned human-readable address/location string or None.
    """
    address_element = card.select_one(ADDRESS)
    if not address_element:
        return None
    text = address_element.get_text(strip=True)
    return text or None


def parse_price(card: Tag) -> Optional[int]:
    """Extract the price in euros as an integer from a listing card.

    Expected behavior (when implemented):
      - Read visible price text, strip symbols (€, dots, spaces), parse to int.
      - Return None if not present.
    """
    raise NotImplementedError("parse_price is a scaffold stub")


def parse_size(card: Tag) -> Optional[int]:
    """Extract the size in square meters as an integer.

    Expected behavior (when implemented):
      - Locate size text (e.g., "85 m²"), normalize, parse to int.
      - Return None if not present.
    """
    raise NotImplementedError("parse_size is a scaffold stub")


def parse_bathrooms(card: Tag) -> Optional[int]:
    """Extract the number of bathrooms as an integer.

    Expected behavior (when implemented):
      - Locate bathrooms count (e.g., icon+text or stats list), parse to int.
      - Return None if not present.
    """
    raise NotImplementedError("parse_bathrooms is a scaffold stub")


def parse_floor_number(card: Tag) -> Optional[int]:
    """Extract the floor number as an integer when available.

    Expected behavior (when implemented):
      - Handle Spanish terms like "planta", ordinal suffixes ("ª", "º").
      - Map special cases like "Bajo"/"Entresuelo" to conventional integers
        only if you define a consistent mapping; otherwise return None.
    """
    raise NotImplementedError("parse_floor_number is a scaffold stub")


# -----------------------------
# Helpers (cleaning/parsing primitives)
# -----------------------------
def clean_price_text_to_int(text: str) -> Optional[int]:
    """Turn raw price text into an integer EUR value.

    Example inputs: "325.000 €", "1.250 €/mes" → 325000 / 1250 (ignore period separators).
    Implementation intentionally omitted here.
    """
    raise NotImplementedError("clean_price_text_to_int is a scaffold stub")


def extract_int(text: str) -> Optional[int]:
    """Extract the first integer found in a string, or None.

    Example: "85 m²" → 85
    Implementation intentionally omitted here.
    """
    raise NotImplementedError("extract_int is a scaffold stub")


def normalize_ws(text: Optional[str]) -> Optional[str]:
    """Normalize whitespace in a string, preserving None.

    Implementation intentionally omitted here.
    """
    raise NotImplementedError("normalize_ws is a scaffold stub")
