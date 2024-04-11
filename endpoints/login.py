from flask import request, jsonify

from Config import Config
from flask_app import app, bcrypt
from authentication import generate_token


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.json
        username = data.get("username")
        password = data.get("password")
        with Config.users_path.open() as file:
            while user := file.readline().strip():
                db_username, db_password, *_ = user.split()
                if username == db_username and bcrypt.check_password_hash(
                    db_password, password
                ):
                    token = generate_token(username)
                    return jsonify({"token": token}), 200
                if username == user.split()[0]:
                    break
            return jsonify({"error": "Invalid username or password"}), 401
