from functools import wraps
from flask import request, g, jsonify, redirect
import jwt
from utils.jwt_utils import decode

from db import db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return jsonify({"message": "로그인이 필요합니다"}), 401
        try:
            payload = decode(token)
            email = payload.get("email")
            g.user_email = email
            user = db.users.find_one({"email": email})
            if not user:
                return jsonify({"message": "로그인이 필요합니다"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "토큰이 만료되었습니다"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "유효하지 않은 토큰입니다"}), 401

        return f(*args, **kwargs)

    return decorated_function


def login_required_html(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect("/login")

        try:
            payload = decode(token)
            email = payload.get("email")
            g.user_email = email
            user = db.users.find_one({"email": email})
            if not user:
                return redirect("/login")
        except jwt.ExpiredSignatureError:
            return redirect("/login")
        except jwt.InvalidTokenError:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated
