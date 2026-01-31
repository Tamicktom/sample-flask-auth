# Libraries imports
from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)

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
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.post("/login")
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Login realizado com sucesso"}), 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout feito com sucesso"})


@app.post("/sign-up")
def sign_up():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário cadastrado com sucesso"}), 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.get("/user/<int:id>")
def get_user(id: int):
    user = User.query.get(id)

    if user:
        return jsonify({"message": "Usuário encontrado", "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404


@app.get("/hello")
def hello_world():
    return jsonify({"message": "Hello world"})


if __name__ == "__main__":
    app.run(debug=True)
