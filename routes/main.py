from flask import Blueprint, render_template

main_route = Blueprint("main", __name__, template_folder="templates")


@main_route.route("/")
def index():
    return render_template("index.html")


@main_route.route("/login")
def login():
    return render_template("login.html")


@main_route.route("/signup")
def signup():
    return render_template("signup.html")
