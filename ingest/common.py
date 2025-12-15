"""Common scraper utils"""

from __future__ import annotations

from time import sleep
from typing import Final
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL: Final = "https://malegislature.gov"


def fetch_html(path_or_url: str, *, delay_seconds: float = 0.5) -> str:
    """Fetch a page relative to the URL"""
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = urljoin(BASE_URL, path_or_url)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    sleep(delay_seconds)
    return resp.text


def get_soup(path_or_url: str) -> BeautifulSoup:
    """Gets the structured content of a page"""
    html = fetch_html(path_or_url)
    return BeautifulSoup(html, "html.parser")
