# Shopify Smart Collection Creator

This Python script creates a smart collection in a Shopify store containing products without a specific tag. It adds an alternative tag to products that do not have the specific tag and creates a smart collection that includes products with the alternative tag.

## Requirements

- Python 3.7 or higher
- `requests` library
- `python-dotenv` library

## Setup

1. Clone this repository or download the script.

2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Create a .env file in the same directory as your script with the following content:

```env
STORE_URL=https://your-store.myshopify.com/admin/api/2023-01
ACCESS_TOKEN=your-access-token
```

Replace your-store.myshopify.com and your-access-token with your store's URL and access token.

4. Open the script and update the specific_tag and alternative_tag variables with the tags you want to use for filtering products and creating the smart collection:

```python
specific_tag = 'your-specific-tag'
alternative_tag = 'alternative_tag'
```

Replace your-specific-tag with the tag you want to filter out and Not_New with the alternative tag you want to add to products without the specific tag.

## Usage

Execute the script from the command line:

```bash
python smart_collection_creator.py
```

The script will:

- Retrieve all products in your Shopify store
- Update the tags for products without the specific tag to include the alternative tag
- Create a new smart collection containing products with the alternative tag
- Check your Shopify store's collections to see the new smart collection.

## Functions

`get_all_products()`

Retrieves all products from the Shopify store using cursor-based pagination.

***Returns***

`list` - A list of all products in the store as dictionaries.

`create_smart_collection(title, tag_to_include)`
Creates a smart collection in the Shopify store with the specified title and a rule to include products with a specific tag.

***Parameters***

- `title` (str) - The title of the smart collection.
- `tag_to_include` (str) - The tag to include in the smart collection rule.

***Returns***

- `init` or `None` - The ID of the created smart collection, or None if the creation failed.

`update_product_tags(product_id, new_tags)`

Updates the tags of a product in the Shopify store.

***Parameters***

- `product_id` (int) - The ID of the product to update.
- `new_tags` (str) - The new tags for the product as a comma-separated string.
