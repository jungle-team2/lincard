from flask import Flask, g, request

import jwt
from utils.jwt_utils import decode

app = Flask(__name__)
app.secret_key = "some_secret_key"

from routes.main import main
from api.auth import auth_api

app.register_blueprint(main)
app.register_blueprint(auth_api, url_prefix="/api/auth")


@app.before_request
def load_logged_in_user():
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = decode(token)
            g.user_email = payload.get("email")
        except jwt.ExpiredSignatureError:
            g.user_id = None
        except jwt.InvalidTokenError:
            g.user_id = None


@app.context_processor
def inject_logged_in():
    return {
        "logged_in": hasattr(g, "user_email"),
    }


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
