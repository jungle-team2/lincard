from flask import Flask, render_template

app = Flask(__name__)

from routes.main import main_route
from api.auth import auth_api

app.register_blueprint(main_route)
app.register_blueprint(auth_api, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
