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
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        for a in pagination.find_all('a'):
            href = a.get('href')
            if href:
                pages.add(resolve_url(base_url, href))
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
