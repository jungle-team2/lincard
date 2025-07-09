from flask import Blueprint, render_template, g, request
from middlewares.auth_required import login_required_html
from typing import List, Dict
from dto.users import ProfileDTO
from utils.recommends import find_recommends, find_my_recommends

main = Blueprint("main", __name__, template_folder="templates")

from db import db

usersCollection = db["users"]


# ?userId=123&userId=456
@main.route("/")
def index():
    # random user

    users: List[str] = request.args.getlist("userId")  # ['abc', 'def']
    # list가 비어있을땐 그냥 진행

    pipeline = get_random_user_pipeline(users)
    random_user = list(usersCollection.aggregate(pipeline))

    # if not random_user:
    #     return render_template("index.html", feed=None) 없을경우 어떻게 처리할건지 논의

    random_user = random_user[0]
    print(random_user)
    feed = ProfileDTO(
        userId=str(random_user["_id"]),
        introduction=random_user["introduction"],
        data=random_user["data"],
    )
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


def get_random_user_pipeline(users: List[str]) -> List[Dict[str, any]]:
    return [{"$match": {"_id": {"$nin": users}}}, {"$sample": {"size": 1}}]


@main.route("/mypage/recommends")
@login_required_html
def my_recommends():
    recommends = find_my_recommends()
    return render_template("my_recommends.html", recommends=recommends)
