from flask import Blueprint, render_template, g
from middlewares.auth_required import login_required_html

main = Blueprint("main", __name__, template_folder="templates")

from db import db


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/signup")
def signup():
    return render_template("signup.html")


@main.route("/mypage")
@login_required_html
def mypage():
    user_email = g.user_email
    user = db.users.find_one({"email": user_email})
    return render_template("mypage.html", user=user)
