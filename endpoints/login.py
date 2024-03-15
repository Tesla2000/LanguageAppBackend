from flask import request, jsonify

from app import app
from authentication import generate_token


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        users

        if username in users and users[username]['password'] == password:
            # Successful login, generate and return token
            token = generate_token(username)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401