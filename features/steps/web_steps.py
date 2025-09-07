import requests
from behave import when, then
from compare import expect


@when('I visit the "home page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.resp = requests.get(context.BASE_URL)


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set an element to a text string"""
    context.element_name = element_name
    context.text_string = text_string


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button on the page"""
    if button == 'Search':
        # Handle search functionality
        if context.element_name == 'name':
            context.resp = requests.get(f"{context.BASE_URL}/products?name={context.text_string}")
        elif context.element_name == 'category':
            context.resp = requests.get(f"{context.BASE_URL}/products?category={context.text_string}")
        elif context.element_name == 'available':
            available_value = context.text_string.lower() in ['true', 'yes', '1']
            context.resp = requests.get(f"{context.BASE_URL}/products?available={str(available_value).lower()}")
    elif button == 'Create':
        # Handle create functionality
        data = {
            "name": context.text_string if context.element_name == 'name' else 'Test Product',
            "description": 'Test Description',
            "price": 99.99,
            "available": True,
            "category": context.text_string if context.element_name == 'category' else 'Electronics'
        }
        context.resp = requests.post(f"{context.BASE_URL}/products", json=data)
    elif button == 'Update':
        # Handle update functionality
        if hasattr(context, 'product_id'):
            data = {
                "name": context.text_string if context.element_name == 'name' else 'Updated Product',
                "description": 'Updated Description',
                "price": 149.99,
                "available": True,
                "category": context.text_string if context.element_name == 'category' else 'Electronics'
            }
            context.resp = requests.put(f"{context.BASE_URL}/products/{context.product_id}", json=data)
    elif button == 'Delete':
        # Handle delete functionality
        if hasattr(context, 'product_id'):
            context.resp = requests.delete(f"{context.BASE_URL}/products/{context.product_id}")
    elif button == 'List All':
        # Handle list all functionality
        context.resp = requests.get(f"{context.BASE_URL}/products")


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check for a message in the response"""
    if context.resp.status_code >= 400:
        # For error responses, check the error message
        error_data = context.resp.json()
        expect(error_data).to(have_key('message'))
        expect(error_data['message']).to(contain(message))
    else:
        # For success responses, check if message matches expected format
        if message == "Success":
            expect(context.resp.status_code).to(be_less_than(400))


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Check if a name appears in the search results"""
    expect(context.resp.status_code).to(equal(200))
    data = context.resp.json()
    found = False
    for product in data:
        if name in product.get('name', ''):
            found = True
            break
    expect(found).to(be_true)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Check if a name does not appear in the search results"""
    expect(context.resp.status_code).to(equal(200))
    data = context.resp.json()
    found = False
    for product in data:
        if name in product.get('name', ''):
            found = True
            break
    expect(found).to(be_false)


@when('I retrieve the "{product_name}" product')
def step_impl(context, product_name):
    """Retrieve a specific product by name"""
    context.resp = requests.get(f"{context.BASE_URL}/products?name={product_name}")
    if context.resp.status_code == 200:
        products = context.resp.json()
        if products:
            context.product_id = products[0]['id']
            context.resp = requests.get(f"{context.BASE_URL}/products/{context.product_id}")


@then('I should see "{text}" in the title')
def step_impl(context, text):
    """Check if text appears in the page title or response"""
    if context.resp.status_code == 200:
        data = context.resp.json()
        if isinstance(data, dict):
            # Single product response
            found = any(text in str(value) for value in data.values())
            expect(found).to(be_true)
        elif isinstance(data, list):
            # Multiple products response
            expect(len(data)).to(be_greater_than(0))


@then('I should not see "{text}" in the title')
def step_impl(context, text):
    """Check if text does not appear in the page title or response"""
    if context.resp.status_code == 200:
        data = context.resp.json()
        if isinstance(data, dict):
            # Single product response
            found = any(text in str(value) for value in data.values())
            expect(found).to(be_false)
        elif isinstance(data, list):
            # Multiple products response should be empty
            expect(len(data)).to(equal(0))