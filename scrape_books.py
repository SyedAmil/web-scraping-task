"""
Task 1: Web Scraping
Scrapes all ~1,000 books from books.toscrape.com (a public site built for
scraping practice) and saves a clean custom dataset to books_dataset.csv.

Setup:  pip install requests beautifulsoup4
Run:    python scrape_books.py
"""
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT = "books_dataset.csv"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (student scraping project)"


def parse_page(soup, page_url):
    """Extract one record per book on a listing page."""
    rows = []
    for card in soup.select("article.product_pod"):
        link = card.h3.a
        rating_word = card.select_one("p.star-rating")["class"][1]
        rows.append({
            "title": link["title"],
            "price_gbp": float(card.select_one("p.price_color").text.replace("£", "").replace("Â", "")),
            "rating": RATINGS.get(rating_word),
            "in_stock": "In stock" in card.select_one("p.availability").text,
            "url": urljoin(page_url, link["href"]),
        })
    return rows


def scrape():
    url, data, page = START_URL, [], 1
    while url:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        data.extend(parse_page(soup, url))
        print(f"Page {page}: {len(data)} books so far")

        # Navigation: follow the "next" button until it disappears
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        page += 1
        time.sleep(0.5)  # be polite to the server
    return data


def save(rows):
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    save(scrape())