# Libraries imports
from pathlib import Path

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

# Project root: src/app/__init__.py -> parent.parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INSTANCE_PATH = PROJECT_ROOT / "instance"
INSTANCE_PATH.mkdir(exist_ok=True)
DATABASE_PATH = INSTANCE_PATH / "database.db"

app = Flask(__name__, instance_path=str(INSTANCE_PATH))
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"

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
@login_required  # only authenticated users can access this route
def get_user(id: int):
    user = User.query.get(id)

    if user:
        return (
            jsonify(
                {
                    "message": "Usuário encontrado",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "password": user.password,
                    },
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404


@app.put("/user/<int:id>")
@login_required  # only authenticated users can access this route
def update_user(id: int):
    data = request.json

    user = User.query.get(id)

    # If user is not found
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    is_same_user = user.id == current_user.id

    # if is not the same user
    if not is_same_user:
        return (
            jsonify({"message": "Você não tem permissão para atualizar este usuário"}),
            403,
        )

    username = data.get("username")
    password = data.get("password")

    # check if the new username is avaliable
    username_owner = User.query.filter_by(username=username).first()
    if username_owner:
        return jsonify({"message": "Username já está sendo utilizado"}), 400

    if username:
        user.username = username
    if password:
        user.password = password

    db.session.commit()

    return jsonify({"message": f"Usuário {id} atualizado com sucesso"}), 200


@app.delete("/user/<int:id>")
@login_required
def delete_user(id: int):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Usuário {id} deletado com sucesso"}), 200


@app.get("/hello")
def hello_world():
    return jsonify({"message": "Hello world"})


if __name__ == "__main__":
    app.run(debug=True)
