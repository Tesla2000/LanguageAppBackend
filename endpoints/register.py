from flask import request, jsonify

from database.create_user import create_user
from flask_app import app, bcrypt


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    try:
        create_user(username, bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    except AssertionError:
        return jsonify({"error": "Username already exists"}), 400
    return jsonify({"message": "User registered successfully"}), 201
