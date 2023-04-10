import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Replace with your store's URL, access token, and the tag to filter
store_url = os.getenv('STORE_URL')
access_token = os.getenv('ACCESS_TOKEN')
specific_tag = 'specific_tag'
alternative_tag = 'alternative_tag'

headers = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': access_token,
}


def get_all_products():
    products = []
    limit = 250
    cursor = None

    while True:
        products_url = f'{store_url}/products.json?limit={limit}'
        if cursor:
            products_url += f'&page_info={cursor}'
        
        products_response = requests.get(products_url, headers=headers)
        current_products = products_response.json().get('products', [])

        if not current_products:
            break

        products.extend(current_products)
        link_header = products_response.headers.get('Link')

        if not link_header:
            break

        next_link = [link for link in link_header.split(', ') if 'rel="next"' in link]

        if not next_link:
            break

        cursor = next_link[0].split(';')[0].strip('<>').split('page_info=')[1]

    return products

def create_smart_collection(title, tag_to_include):
    smart_collections_url = f'{store_url}/smart_collections.json'
    payload = {
        'smart_collection': {
            'title': title,
            'rules': [
                {
                    'column': 'tag',
                    'relation': 'equals',
                    'condition': tag_to_include
                }
            ]
        }
    }
    response = requests.post(smart_collections_url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json().get('smart_collection', {}).get('id')
    else:
        print(f"Error creating smart collection: {response.status_code} {response.text}")
        return None

def update_product_tags(product_id, new_tags):
    product_url = f'{store_url}/products/{product_id}.json'
    payload = {
        'product': {
            'id': product_id,
            'tags': new_tags
        }
    }
    response = requests.put(product_url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Error updating product tags for product {product_id}: {response.status_code} {response.text}")

# Retrieve all products using cursor-based pagination
all_products = get_all_products()

# Update the tags for products without the specific tag
for product in all_products:
    tags = product['tags'].split(', ')
    if specific_tag not in tags:
        new_tags = ', '.join(tags + [alternative_tag])
        update_product_tags(product['id'], new_tags)

# Create a new smart collection
collection_title = 'Spring35'
collection_id = create_smart_collection(collection_title, alternative_tag)

if collection_id:
    print(f'Created a new smart collection "{collection_title}" with products without the "{specific_tag}" tag.')
else:
    print(f"Failed to create smart collection '{collection_title}'.")
