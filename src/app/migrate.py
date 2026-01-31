from database import db

# Create all tables
db.create_all()

# Commit the changes
db.session.commit()