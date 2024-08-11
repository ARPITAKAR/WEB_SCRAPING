import httpx
from selectolax.parser import HTMLParser
import pandas as pd

def get_html(baseurl, page):
    # Fetch the HTML content
    response = httpx.get(baseurl + str(page), follow_redirects=True)
    response.raise_for_status()  # Ensure the request was successful
    html_content = response.text

    # Parse the HTML content
    html = HTMLParser(html_content)
    return html

def parse_page(html):
    # Select the div with class collection__products
    collection_divs = html.css('div.collection__products')

    # Initialize lists to store extracted data
    products = []

    # Iterate over each product-item within the collection
    for collection in collection_divs:
        # Select all product items within the collection
        product_items = collection.css('div.product-item__price__holder')
        
        for item in product_items:
            # Extract product cutline (if needed)
            cutline = item.css_first('span.product-item__cutline').text(strip=True) if item.css_first('span.product-item__cutline') else 'Not available'
            
            # Extract the sale price
            price_span = item.css_first('span.price.sale')
            new_price = price_span.css_first('span.new-price').text(strip=True) if price_span.css_first('span.new-price') else 'Not available'
            old_price = price_span.css_first('span.old-price').text(strip=True) if price_span.css_first('span.old-price') else 'Not available'

            # Append the product data to the list
            products.append({
                'Product': cutline,
                'Sale Price': new_price,
                'Regular Price': old_price
            })

    return products

def main():
    all_products = []
    
    for x in range(1, 8):
        baseurl = 'https://www.eyewearlabs.com/collections/sunglasses-for-men?page='
        html = get_html(baseurl, x)
        products = parse_page(html)
        all_products.extend(products)

    # Create a DataFrame from all the extracted data
    df = pd.DataFrame(all_products)
    # Save the DataFrame as a CSV file
    df.to_csv('sunglass_datasets.csv', index=False)  # Change 'products.csv' to your desired filename and path

    # Optionally print a message to confirm
    print("DataFrame saved as 'products.csv'")
if __name__ == "__main__":
    main()
