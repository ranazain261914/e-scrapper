from .utils import fetch_page
from .parsers import parse_sidebar_links, parse_pagination, parse_product_links, parse_product_details
import logging

class Crawler:
    """Main crawler class to navigate e-commerce site and extract products"""
    
    def __init__(self, start_url):
        self.start_url = start_url
        self.base_url = "https://webscraper.io"
        self.products = []
        self.seen_product_urls = set()
        self.duplicates_removed = 0

    def run(self):
        """Start the crawling process"""
        logging.info("Starting crawler...")
        html = fetch_page(self.start_url)
        if not html:
            return
        
        categories = parse_sidebar_links(html, self.base_url)
        for cat_name, cat_url in categories:
            self.crawl_category(cat_name, cat_url)

    def crawl_category(self, cat_name, cat_url):
        """Crawl a category and discover subcategories"""
        logging.info(f"Crawling Category: {cat_name}")
        html = fetch_page(cat_url)
        if not html:
            return
        
        subcats = parse_sidebar_links(html, self.base_url)
        has_subcats = False
        
        for sub_name, sub_url in subcats:
            if sub_url != cat_url and cat_url in sub_url:
                has_subcats = True
                self.crawl_subcategory(cat_name, sub_name, sub_url)
        
        if not has_subcats:
            self.crawl_subcategory(cat_name, cat_name, cat_url)

    def crawl_subcategory(self, cat_name, sub_name, sub_url):
        """Crawl a subcategory and handle pagination"""
        logging.info(f"Crawling Subcategory: {sub_name}")
        html = fetch_page(sub_url)
        if not html:
            return
        
        pages = parse_pagination(html, self.base_url)
        if sub_url not in pages:
            pages.append(sub_url)
        
        for page_url in pages:
            self.crawl_listing_page(cat_name, sub_name, page_url)

    def crawl_listing_page(self, cat_name, sub_name, page_url):
        """Crawl a listing page and extract product detail page links"""
        logging.info(f"Scraping Listing Page: {page_url}")
        html = fetch_page(page_url)
        if not html:
            return
        
        product_links = parse_product_links(html, self.base_url)
        for p_url in product_links:
            if p_url in self.seen_product_urls:
                self.duplicates_removed += 1
                continue
            self.seen_product_urls.add(p_url)
            self.scrape_product_detail(cat_name, sub_name, page_url, p_url)

    def scrape_product_detail(self, cat_name, sub_name, page_url, p_url):
        """Scrape individual product detail page"""
        logging.info(f"Scraping Product: {p_url}")
        html = fetch_page(p_url)
        if not html:
            return
        
        product_data = parse_product_details(html, p_url, cat_name, sub_name, page_url)
        self.products.append(product_data)
