import os
import logging
import unittest
from service.models import Product, DataValidationError, db, app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        with app.app_context():
            db.session.close()

    def setUp(self):
        """This runs before each test"""
        with app.app_context():
            db.session.query(Product).delete()
            db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        with app.app_context():
            db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        with app.app_context():
            product = Product(name="Laptop", description="Gaming Laptop", price=999.99, available=True, category="Electronics")
            self.assertEqual(str(product), "<Product Laptop id=[None]>")
            self.assertTrue(product is not None)
            self.assertEqual(product.id, None)
            self.assertEqual(product.name, "Laptop")
            self.assertEqual(product.description, "Gaming Laptop")
            self.assertEqual(product.price, 999.99)
            self.assertEqual(product.available, True)
            self.assertEqual(product.category, "Electronics")

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        with app.app_context():
            products = Product.all()
            self.assertEqual(products, [])
            product = Product(name="Laptop", description="Gaming Laptop", price=999.99, available=True, category="Electronics")
            self.assertTrue(product is not None)
            self.assertEqual(product.id, None)
            product.create()
            self.assertIsNotNone(product.id)
            products = Product.all()
            self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a Product"""
        with app.app_context():
            product = ProductFactory()
            product.id = None
            product.create()
            self.assertIsNotNone(product.id)
            # Fetch it back
            found_product = Product.find(product.id)
            self.assertEqual(found_product.id, product.id)
            self.assertEqual(found_product.name, product.name)
            self.assertEqual(found_product.description, product.description)
            self.assertEqual(found_product.price, product.price)
            self.assertEqual(found_product.available, product.available)
            self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a Product"""
        with app.app_context():
            product = ProductFactory()
            product.id = None
            product.create()
            self.assertIsNotNone(product.id)
            # Change it and save it
            product.category = "Electronics"
            original_id = product.id
            product.update()
            self.assertEqual(product.id, original_id)
            self.assertEqual(product.category, "Electronics")
            # Fetch it back and make sure the id hasn't changed
            # but the data did change
            products = Product.all()
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0].id, original_id)
            self.assertEqual(products[0].category, "Electronics")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        with app.app_context():
            product = ProductFactory()
            product.create()
            self.assertEqual(len(Product.all()), 1)
            # delete the product and make sure it isn't in the database
            product.delete()
            self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        with app.app_context():
            products = Product.all()
            self.assertEqual(products, [])
            # Create 5 Products
            for _ in range(5):
                product = ProductFactory()
                product.create()
            # See if we get back 5 products
            products = Product.all()
            self.assertEqual(len(products), 5)

    def test_find_product_by_name(self):
        """It should Find a Product by Name"""
        with app.app_context():
            products = ProductFactory.create_batch(5)
            for product in products:
                product.create()
            name = products[0].name
            count = len([product for product in products if product.name == name])
            found = Product.find_by_name(name)
            self.assertEqual(found.count(), count)
            for product in found:
                self.assertEqual(product.name, name)

    def test_find_product_by_category(self):
        """It should Find Products by Category"""
        with app.app_context():
            products = ProductFactory.create_batch(10)
            for product in products:
                product.create()
            category = products[0].category
            count = len([product for product in products if product.category == category])
            found = Product.find_by_category(category)
            self.assertEqual(found.count(), count)
            for product in found:
                self.assertEqual(product.category, category)

    def test_find_product_by_availability(self):
        """It should Find Products by Availability"""
        with app.app_context():
            products = ProductFactory.create_batch(10)
            for product in products:
                product.create()
            available = products[0].available
            count = len([product for product in products if product.available == available])
            found = Product.find_by_availability(available)
            self.assertEqual(found.count(), count)
            for product in found:
                self.assertEqual(product.available, available)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        with app.app_context():
            product = ProductFactory()
            data = product.serialize()
            self.assertNotEqual(data, None)
            self.assertIn("id", data)
            self.assertEqual(data["id"], product.id)
            self.assertIn("name", data)
            self.assertEqual(data["name"], product.name)
            self.assertIn("description", data)
            self.assertEqual(data["description"], product.description)
            self.assertIn("price", data)
            self.assertEqual(data["price"], product.price)
            self.assertIn("available", data)
            self.assertEqual(data["available"], product.available)
            self.assertIn("category", data)
            self.assertEqual(data["category"], product.category)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        with app.app_context():
            data = ProductFactory().serialize()
            product = Product()
            product.deserialize(data)
            self.assertNotEqual(product, None)
            self.assertEqual(product.id, None)
            self.assertEqual(product.name, data["name"])
            self.assertEqual(product.description, data["description"])
            self.assertEqual(product.price, data["price"])
            self.assertEqual(product.available, data["available"])
            self.assertEqual(product.category, data["category"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        with app.app_context():
            data = {"id": 1, "name": "Laptop", "description": "Gaming Laptop"}
            product = Product()
            with self.assertRaises(DataValidationError):
                product.deserialize(data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        with app.app_context():
            product = Product()
            with self.assertRaises(DataValidationError):
                product.deserialize("this is not a dictionary")

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        with app.app_context():
            test_product = ProductFactory()
            data = test_product.serialize()
            data["available"] = "true"
            product = Product()
            with self.assertRaises(DataValidationError):
                product.deserialize(data)