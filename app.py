from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "some_secret_key"

from routes.main import main
from api.auth import auth_api

app.register_blueprint(main)
app.register_blueprint(auth_api, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
