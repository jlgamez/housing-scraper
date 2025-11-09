# Project Context: housing Neighborhood Scraper

## Overview
This project builds a **lightweight scraper for [fotocasa.es](https://www.fotocasa.es/)** to extract summarized property data for a given **neighborhood** without entering individual listings.  
The scraper uses **`requests` + `BeautifulSoup`** for simplicity and control, with small random delays to avoid detection.  

---

## Purpose
Given a neighborhood or search URL, the scraper should:
1. **Paginate** through all available result pages.
2. For each listing **card** (not detail pages), extract:
   - `title` — listing headline or summary text.
   - `price` — numeric value in euros.
   - `location` — neighborhood or short address.
   - `floor` — floor number or position (e.g. “3ª planta”, “Bajo”).
   - `has_elevator` — boolean flag (`true` if “ascensor” is mentioned in features/icons).

The final data should be exportable to **JSON/CSV** and can later be used for market analysis or as training data for ML prototypes (non-commercial unless explicitly approved by fotocasa).

---

## Scope & Constraints
- **Do not scrape individual listing pages.**
- **No personal data (names, contacts, phone numbers, etc.).**
- **Lightweight footprint:** respect robots.txt and avoid aggressive crawling.
- **Goal:** simplicity, stability, and low detection risk — not maximum throughput.

---

## Architecture Overview

### 1. Core Components
- **HTTP client:** `requests` for simple, efficient HTTP calls.  
- **HTML parser:** `BeautifulSoup` (`lxml` parser) for robust HTML traversal.  
- **Storage:** JSON and/or CSV exports.
- **Anti-detection layer:** randomized sleeps, rotating headers, and optional proxy rotation.

### 2. Pagination Strategy
- Identify pagination pattern in URLs (e.g., `/pagina-2.htm` or query param `?pagina=2`).
- Continue fetching sequentially until:
  - No listings are found, or
  - Empty result page / 404 encountered.

### 3. Data Extraction Logic
For each card element in the HTML:
- Extract visible text fields.
- Clean numeric data (remove `€`, spaces, or punctuation).
- Parse floor level using regex for keywords (`planta`, `bajo`, `entresuelo`, `ª`, `º`).
- Detect “ascensor” text or icon alt/title → `has_elevator = true`.

---

## Anti-Detection Strategy
Light, respectful scraping practices:
- Randomized short sleeps between requests (`0.5–2.5s` typical).
- Add occasional longer pauses every few pages.
- Rotate **User-Agent** and **Accept-Language (es-ES)** headers.
- Use persistent sessions to reuse cookies.
- Optional use of **residential proxies** if scaling up.
- On 403/429, apply exponential backoff and retry later.

If fotocasa starts requiring JavaScript rendering or protection, migrate the HTTP layer to **Playwright** for stealth browser emulation.

---

## Playwright (Optional Future Upgrade)
If fotocasa pages become JavaScript-rendered or protected by anti-bot systems:
- Switch to **Playwright** for page rendering and navigation.
- Playwright offers better stealth and speed than Selenium.
- Integrate it minimally — only for pages that fail to load statically.

---

## Operational Guidelines
- Save sample HTML responses for parser debugging.
- Use structured logging (page number, URL, response status).
- Deduplicate by unique listing URL or ID.
- Store config (headers, proxies, delays) in a `.env` file or YAML.

---

## Legal & Ethical Notes
- fotocasa’s Terms of Service **forbid automated scraping** for commercial use without permission.  
- Use data responsibly for **research and prototyping only**.
- Avoid collecting or storing personal data to comply with GDPR and ethical standards.

---

## Future Extensions
- Add CLI or small API wrapper to trigger scrapes by neighborhood name.
- Integrate rotating proxies (e.g. ScraperAPI, ScrapingBee).
- Optional Playwright fallback for JS-rendered pages.
- Store data in SQLite or Postgres for later analysis.

---

## Key Principles
1. **Simplicity first** — minimal dependencies, fast iteration.  
2. **Respectful scraping** — human-like pace, proper headers.  
3. **Maintainability** — clean modular code (fetch → parse → store).  
4. **Extendability** — easy to upgrade to Playwright or Scrapy if scaling up.

---

## Example Data Schema (JSON)
```json
{
  "title": "Piso en venta en Calle Mayor",
  "price": 325000,
  "location": "Barrio de Salamanca, Madrid",
  "floor": "3ª planta",
  "has_elevator": true,
  "url": "https://www.fotocasa
.es/inmueble/12345678/"
}
