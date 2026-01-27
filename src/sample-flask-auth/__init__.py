# Libraries imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


@app.get("/hello")
def hello_world():
    return jsonify({"message": "Hello world"})


if __name__ == "__main__":
    app.run(debug=True)
