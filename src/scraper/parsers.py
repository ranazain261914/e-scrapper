from bs4 import BeautifulSoup
from .utils import clean_text, clean_price, resolve_url

def parse_sidebar_links(html, base_url):
    """Extract category/subcategory links from sidebar menu"""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    menu = soup.find('ul', id='side-menu')
    if menu:
        for a in menu.find_all('a'):
            href = a.get('href')
            if href and '/static/' in href and href != '/test-sites/e-commerce/static':
                links.append((clean_text(a.text), resolve_url(base_url, href)))
    return links

def parse_pagination(html, base_url):
    """Extract pagination links from listing pages"""
    soup = BeautifulSoup(html, 'html.parser')
    pages = set()
    
    # First, try to extract pagination links from the HTML
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        for a in pagination.find_all('a'):
            href = a.get('href')
            if href and 'page=' in href:
                pages.add(resolve_url(base_url, href))
    
    # Also check for item count to generate all pages programmatically
    item_count_elem = soup.find('p', class_='item-count')
    if item_count_elem:
        try:
            # Extract number from "117 items" text
            item_text = item_count_elem.text.strip()
            item_count = int(''.join(filter(str.isdigit, item_text.split()[0])))
            # Calculate total pages (6 items per page is standard for this site)
            items_per_page = 6
            total_pages = (item_count + items_per_page - 1) // items_per_page
            
            # Extract base URL from any existing page link or current URL
            base_page_url = None
            if pagination:
                first_link = pagination.find('a')
                if first_link and first_link.get('href'):
                    href = first_link.get('href')
                    # Remove ?page= part to get base URL
                    base_page_url = href.split('?page=')[0]
            
            # If we couldn't find a page link, use the current URL as base
            if not base_page_url:
                # Assume the current page is the base URL
                current_url = base_url
                # This will be refined by the crawler
                base_page_url = current_url
            
            # Generate all page URLs
            for page_num in range(1, total_pages + 1):
                if page_num == 1:
                    # First page might not have ?page=1 parameter
                    pages.add(resolve_url(base_url, base_page_url))
                else:
                    page_url = f"{base_page_url}?page={page_num}"
                    pages.add(resolve_url(base_url, page_url))
        except (ValueError, IndexError):
            pass
    
    return list(pages)

def parse_product_links(html, base_url):
    """Extract product links from listing pages"""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a in soup.find_all('a', class_='title'):
        href = a.get('href')
        if href:
            links.append(resolve_url(base_url, href))
    return links

def parse_product_details(html, url, category, subcategory, source_page):
    """Parse product details from product detail page"""
    soup = BeautifulSoup(html, 'html.parser')
    
    title_elem = soup.find('h4', class_='title') or soup.find('h4', string=True)
    title = clean_text(title_elem.text) if title_elem else "Unknown"
    
    price_elem = soup.find('h4', class_='price')
    price = clean_price(price_elem.text) if price_elem else 0.0
    
    desc_elem = soup.find('p', class_='description')
    description = clean_text(desc_elem.text) if desc_elem else ""
    
    review_elem = soup.find('p', class_='review-count')
    review_count = clean_text(review_elem.text) if review_elem else "0 reviews"
    
    rating_elem = soup.find('p', {'data-rating': True})
    rating = rating_elem['data-rating'] if rating_elem else ""
    
    swatches = soup.find('div', class_='swatches')
    spec = clean_text(swatches.text) if swatches else ""
    
    image_elem = soup.find('img', class_='img-responsive')
    image_url = resolve_url(url, image_elem['src']) if image_elem and 'src' in image_elem.attrs else ""

    return {
        'category': category,
        'subcategory': subcategory,
        'title': title,
        'price': price,
        'product_url': url,
        'image_url': image_url,
        'description': description,
        'review_count': review_count,
        'spec': spec,
        'source_page': source_page
    }
