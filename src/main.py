from scraper.crawler import Crawler
from scraper.exporters import export_products, export_summary
import os

def main():
    """Main entry point for the scraper"""
    target_url = "https://webscraper.io/test-sites/e-commerce/static"
    crawler = Crawler(target_url)
    
    print("Starting Web Scraper...")
    crawler.run()
    print(f"Scraping complete. Extracted {len(crawler.products)} unique products.")
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    products_file = os.path.join(data_dir, 'products.csv')
    summary_file = os.path.join(data_dir, 'category_summary.csv')
    
    export_products(crawler.products, products_file)
    export_summary(crawler.products, summary_file, crawler.duplicates_removed)
    print(f"Data saved to {products_file} and {summary_file}")

if __name__ == "__main__":
    main()
