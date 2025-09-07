import os
from flask import Flask
from service.models import db
from service.routes import app

if __name__ == "__main__":
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)