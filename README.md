# Product Management System

A Flask-based REST API for product management with comprehensive testing including unit tests, integration tests, and BDD scenarios.

## Project Structure

```
product-management/
├── service/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── common/
│       ├── __init__.py
│       └── status.py
├── tests/
│   ├── __init__.py
│   ├── factories.py
│   ├── test_models.py
│   └── test_routes.py
├── features/
│   ├── products.feature
│   └── steps/
│       ├── __init__.py
│       ├── load_steps.py
│       └── web_steps.py
├── requirements.txt
├── app.py
└── README.md
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Factory Boy**: Test data generation
- **Behave**: BDD testing framework
- **Selenium**: Web automation for BDD tests
- **Flask-Testing**: Testing utilities for Flask
- **SQLite**: Database for development and testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd product-management
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### BDD Tests
```bash
behave features/
```

## API Endpoints

- `GET /products` - List all products
- `GET /products/<id>` - Get product by ID
- `POST /products` - Create new product
- `PUT /products/<id>` - Update product
- `DELETE /products/<id>` - Delete product
- `GET /products?name=<name>` - Search by name
- `GET /products?category=<category>` - Search by category
- `GET /products?available=<true/false>` - Search by availability

## Features Tested

- CRUD operations (Create, Read, Update, Delete)
- Product search by name, category, and availability
- Data validation and error handling
- RESTful API compliance