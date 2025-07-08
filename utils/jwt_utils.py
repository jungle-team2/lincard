from flask import g
import jwt

SECRET_KEY = "your_secret_key"


def decode(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # g.user_email = payload.get("email")
    return payload


def encode(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
