from flask import Blueprint, render_template, g
from middlewares.auth_required import login_required_html

main = Blueprint("main", __name__, template_folder="templates")

from db import db


@main.route("/")
def index():
    # random user
    feed = {
        "email": "123@123.com",
        "data": {
            "name": "123",
            "gender": "m",
            "lang": "Python",
            "name1": "123",
            "gender1": "m",
            "lang1": "Python",
        },
        "introduction": "123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest 123-feedtest123-feedtest 123-feedtest 123-feedtest  ",
    }
    return render_template("index.html", feed=feed)


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/signup")
def signup():
    return render_template("signup.html")


@main.route("/mypage")
@login_required_html
def mypage():
    return render_template("mypage.html", user=g.user)
