import os
from pathlib import Path

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
users_unhashed = Path("data/users_unhashed.txt")
if users_unhashed.exists():
    hashed_users = []
    for line in users_unhashed.read_text().splitlines():
        user, password = line.split()
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_users.append(f"{user} {password}")
    Path("data/users.txt").write_text('\n'.join(hashed_users))
    os.remove(users_unhashed)

import endpoints

_ = endpoints
