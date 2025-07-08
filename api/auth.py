from flask import Blueprint

auth_api = Blueprint("auth", __name__)


@auth_api.post("/login")
def login():
    pass


@auth_api.post("/sign-in")
def signIn():
    pass


@auth_api.post("/logout")
def logout():
    pass
