from flask import Flask, g, request

import jwt
from utils.jwt_utils import decode

app = Flask(__name__)
app.secret_key = "some_secret_key"

from routes.main import main
from api.auth import auth_api
from api.user import user_api

app.register_blueprint(main)
app.register_blueprint(auth_api, url_prefix="/api/auth")
app.register_blueprint(user_api, url_prefix="/api/user")

from db import db

@app.before_request
def load_auth():
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = decode(token)
            email = payload.get("email")
            g.user_email = email

            try:
                g.user = db.users.find_one({"email": email})
            except:
                g.user = None
        except jwt.ExpiredSignatureError:
            g.user_id = None
        except jwt.InvalidTokenError:
            g.user_id = None


@app.context_processor
def inject_logged_in():
    email = getattr(g, "user_email", None)
    user = db.users.find_one({"email": email})

    return {
        "logged_in": user,
    }


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
