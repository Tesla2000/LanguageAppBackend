from flask import request, jsonify

from authentication import generate_token
from database.authenticate_user import authenticate_user
from flask_app import app


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if authenticate_user(username, password):
        token = generate_token(username)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid username or password"}), 401
