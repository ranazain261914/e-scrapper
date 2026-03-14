import requests
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def fetch_page(url):
    """Fetch a page and return its HTML content"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def resolve_url(base, relative):
    """Safely resolve relative URLs using urljoin"""
    if not relative:
        return ""
    return urljoin(base, relative)

def clean_text(text):
    """Clean and strip whitespace from text"""
    return text.strip() if text else ""

def clean_price(price_str):
    """Clean price string and convert to float"""
    if not price_str:
        return 0.0
    cleaned = price_str.replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0
