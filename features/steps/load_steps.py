import requests
from behave import given


@given('the following products')
def step_impl(context):
    """Delete all Products and load new ones"""
    
    # List all of the products and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/products"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == 200)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert(context.resp.status_code == 204)

    # load the database with new products
    create_url = f"{context.BASE_URL}/products"
    for row in context.table:
        data = {
            "name": row['name'],
            "description": row['description'],
            "price": float(row['price']),
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        payload = data
        context.resp = requests.post(create_url, json=payload)
        assert context.resp.status_code == 201