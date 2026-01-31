# Import the database
from database import db

# Import the models
from models.user import User

# import the app from the __init__.py file
from __init__ import app

# Create all tables
with app.app_context():
    db.create_all()
    print("Tables created successfully")