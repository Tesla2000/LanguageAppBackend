from flask import request, jsonify

from Config import Config
from app import app


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if all required fields are present
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']

    with Config.users_path.open() as file:
        while user := file.readline().strip():
            if username == user.split()[0]:
                return jsonify({'error': 'Username already exists'}), 400
    with Config.users_path.open('a') as file:
        file.write(f"{username} {data['password']}\n")
    return jsonify({'message': 'User registered successfully'}), 201
