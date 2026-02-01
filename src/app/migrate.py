# Libraries imports
from sqlalchemy import inspect, text

# Local imports
from database import db
from models.user import User
from __init__ import app


with app.app_context():
    db.create_all()
    print("Tables created successfully")
