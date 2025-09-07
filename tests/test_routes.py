import os
import logging
from unittest import TestCase
from service.common import status
from service.models import db, Product
from service.routes import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///test.db"
)


class TestProductService(TestCase):
    """Test Cases for Product Service"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        with app.app_context():
            db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        with app.app_context():
            db.session.query(Product).delete()  # clean up the last tests
            db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        with app.app_context():
            db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            product = ProductFactory()
            response = self.client.post("/products", json=product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test Product"
            )
            new_product = response.get_json()
            product.id = new_product["id"]
            products.append(product)
        return products

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Product Demo REST API Service")

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_product(self):
        """It should Create a new Product"""
        product = ProductFactory()
        response = self.client.post("/products", json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], product.name, "Names does not match")
        self.assertEqual(new_product["description"], product.description, "Descriptions does not match")
        self.assertEqual(float(new_product["price"]), float(product.price), "Prices does not match")
        self.assertEqual(new_product["available"], product.available, "Availability does not match")
        self.assertEqual(new_product["category"], product.category, "Categories does not match")

    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        product = self._create_products(1)[0]
        response = self.client.get(f"/products/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product that's not found"""
        response = self.client.get("/products/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post("/products", json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        new_product["category"] = "Electronics"
        response = self.client.put(f"/products/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["category"], "Electronics")

    def test_update_product_not_found(self):
        """It should not Update a Product that's not found"""
        product = ProductFactory()
        response = self.client.put("/products/0", json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        """It should Delete a Product"""
        products = self._create_products(5)
        product_count = self.get_product_count()
        test_product = products[0]
        response = self.client.delete(f"/products/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"/products/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get("/products")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_product_list_by_category(self):
        """It should Query Products by Category"""
        products = self._create_products(10)
        test_category = products[0].category
        category_products = [product for product in products if product.category == test_category]
        response = self.client.get(f"/products?category={test_category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(category_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["category"], test_category)

    def test_query_product_list_by_name(self):
        """It should Query Products by Name"""
        products = self._create_products(10)
        test_name = products[0].name
        name_products = [product for product in products if product.name == test_name]
        response = self.client.get(f"/products?name={test_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(name_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["name"], test_name)

    def test_query_product_list_by_availability(self):
        """It should Query Products by Availability"""
        products = self._create_products(10)
        available_products = [product for product in products if product.available is True]
        unavailable_products = [product for product in products if product.available is False]
        response = self.client.get("/products?available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(available_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["available"], True)
        response = self.client.get("/products?available=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(unavailable_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product["available"], False)

    def test_create_product_no_data(self):
        """It should not Create a Product with missing data"""
        response = self.client.post("/products", json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no content type"""
        response = self.client.post("/products")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_bad_content_type(self):
        """It should not Create a Product with bad content type"""
        response = self.client.post("/products", data="bad data", content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_bad_available(self):
        """It should not Create a Product with bad available data"""
        product = ProductFactory()
        product_dict = product.serialize()
        product_dict["available"] = "true"
        response = self.client.post("/products", json=product_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_bad_content_type(self):
        """It should not Update a Product with bad content type"""
        product = self._create_products(1)[0]
        response = self.client.put(f"/products/{product.id}", data="bad data", content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    ######################################################################
    # UTILITY FUNCTIONS
    ######################################################################

    def get_product_count(self):
        """save the current number of products"""
        response = self.client.get("/products")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        return len(data)