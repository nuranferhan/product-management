import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key-for-dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a Product
    """
    
    __tablename__ = "products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.String(63), nullable=False)
    
    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"
    
    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be None to generate next primary key
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()
    
    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category,
        }
    
    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.description = data.get("description", "")
            self.price = data["price"]
            self.available = data.get("available", True)
            self.category = data["category"]
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data"
            )
        return self
    
    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()
    
    @classmethod
    def find(cls, by_id):
        """Finds a Product by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return db.session.get(cls, by_id)
    
    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name
        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_category(cls, category):
        """Returns all Products with the given category
        Args:
            category (string): the category of the Products you want to match
        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)
    
    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by their availability
        Args:
            available (bool): True for products that are available
        """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)