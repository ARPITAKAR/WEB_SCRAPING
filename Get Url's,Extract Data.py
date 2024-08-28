import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import time
def get_html(url,**kwargs):
    
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    timeout = httpx.Timeout(60.0)
    if kwargs.get("page"):
        response = httpx.get(url+str(kwargs.get("page")),headers=headers, timeout=timeout,follow_redirects=True)
    else:
        response = httpx.get(url,headers=headers, timeout=timeout,follow_redirects=True)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.page limit exceeded")
        return False
    html=HTMLParser(response.text)
    return html

def parse_page(html):
    # Select all product items
    product_items = html.css('product-item')
    for item in product_items:
        # Find the anchor tag within the product item
        anchor_tag = item.css_first('a.product-item__aspect-ratio')
        
        # Extract the href attribute from the anchor tag
        if anchor_tag:
            product_link = anchor_tag.attrs.get('href')
            yield urljoin("https://sassafras.in",product_link)
def parse_item(html):
    # Extract the product name
    product_name = html.css_first('h1.product-meta__title').text(strip=True) if html.css_first('h1.product-meta__title') else None
    
    # Extract the sale price
    sale_price = html.css_first('span.price--highlight').text(strip=True) if html.css_first('span.price--highlight') else None
    
    # Extract the regular price
    regular_price = html.css_first('span.price--compare').text(strip=True) if html.css_first('span.price--compare') else None

    # Extract the rating
    rating_star = html.css_first('div.rating__stars')
    rating = rating_star.attributes.get('aria-label') if rating_star else None
    
    # Extract any additional rating caption (e.g., "No reviews")
    rating_caption = html.css_first('span.rating__caption').text(strip=True) if html.css_first('span.rating__caption') else None

    # Yield the parsed data as a dictionary
    yield {
        'name': product_name,
        'sale_price': sale_price,
        'regular_price': regular_price,
        'rating': rating,
        'rating_caption': rating_caption
    }
import csv

def export_to_csv(products, filename):
    """
    Exports a list of products to a CSV file with UTF-8 encoding.

    Args:
        products (list of dict): List of products where each product is represented as a dictionary.
        filename (str): The name of the CSV file to export the data.
    """
    # Define CSV fieldnames based on product keys
    fieldnames = ['name', 'sale_price', 'regular_price', 'rating', 'rating_caption']
    
    # Open the file with UTF-8 encoding
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        for product in products:
            writer.writerow(product)  # Write each product as a row in the CSV file
    print(f"Products exported to {filename} in CSV format.")

     
        
def main():
    all_products = []  # List to collect all products

    for x in range(1, 4):  # Assuming we're scraping pages 1 to 3
        baseurl = "https://sassafras.in/collections/mens-t-shirt?page="
        print(f"Scraping page: {x}")
        html = get_html(baseurl, page=x)
        
        if html is False:
            break  # Exit the loop if the request fails
        
        # Parse product links from the current page
        product_links = parse_page(html)
        
        # For each product link, get the product details
        for link in product_links:
            product_html = get_html(link)
            
            # Check if the HTML is valid
            if product_html is None:
                continue

            # Parse the product details
            product_details = list(parse_item(product_html))
            for product in product_details:
                print(product)
                all_products.append(product)  # Add to the list

    # Export all collected products to a CSV file
    export_to_csv(all_products, 'sassafras-products.csv')

if __name__ == "__main__":
    main()
