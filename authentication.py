from datetime import datetime, timedelta

import jwt

from flask import request, abort

from app import app

SECRET_KEY = "L2cRs29YMzIo4FD8TNBSQ2"


def authenticate_token(token):
    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['login']  # Assuming login is stored in the token
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid


@app.before_request
def check_token():
    if request.endpoint in ['get_new_question', 'get_initial_question']:
        if 'Authorization' not in request.headers:
            abort(401)  # Unauthorized if Authorization header is missing

        token = request.headers['Authorization'].split("Bearer ")[-1]
        login = authenticate_token(token)
        if not login:
            abort(401)  # Unauthorized if token is invalid or expired

def generate_token(username):
    # Set expiration time for the token (e.g., 1 day from now)
    expiry = datetime.utcnow() + timedelta(days=1)
    payload = {
        'username': username,
        'exp': expiry
    }
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token.decode()
