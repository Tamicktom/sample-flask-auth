# Libraries imports
from flask import Flask, jsonify, request
from flask_login import LoginManager

# Local imports
from database import db
from models.user import User


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# View Login
@app.post("/login")
def login():
    data = request.json

    return jsonify({"message": "OK"})

@app.get("/hello")
def hello_world():
    return jsonify({"message": "Hello world"})


if __name__ == "__main__":
    app.run(debug=True)
