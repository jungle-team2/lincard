from flask import Blueprint, render_template, g, request, make_response
from middlewares.auth_required import login_required_html
from typing import List, Dict
from dto.users import ProfileDTO
from utils.recommends import find_recommends, find_my_recommends
from bson import ObjectId
import json

main = Blueprint("main", __name__, template_folder="templates")

from db import db

usersCollection = db["users"]


# ?userId=123&userId=456
@main.route("/")
def index():
    recent_raw = request.cookies.get("recent_users", "[]")
    try:
        exclude_ids = json.loads(recent_raw)
    except:
        exclude_ids = []
    # random user

    # users: List[str] = request.args.getlist("userId")  # ['abc', 'def']
    # list가 비어있을땐 그냥 진행

    pipeline = get_random_user_pipeline(exclude_ids)
    random_user = list(usersCollection.aggregate(pipeline))

    # if not random_user:
    #     return render_template("index.html", feed=None) 없을경우 어떻게 처리할건지 논의

    random_user = random_user[0] if random_user else None
    if random_user is None:
        return render_template("index.html", error="모든 유저를 탐색했습니다")

    feed = ProfileDTO(
        userId=str(random_user["_id"]),
        introduction=random_user["introduction"],
        data=random_user["data"],
    )

    if feed.userId not in exclude_ids:
        exclude_ids.append(feed.userId)

    recommends = find_recommends(random_user)

    resp = make_response(
        render_template("index.html", feed=feed, recommends=recommends)
    )
    resp.set_cookie(
        "recent_users", json.dumps(exclude_ids[-5:]), max_age=86400 * 7, path="/"
    )
    return resp


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
    oids = []
    for id in users:
        oids.append(ObjectId(id))
    return [{"$match": {"_id": {"$nin": oids}}}, {"$sample": {"size": 1}}]


@main.route("/mypage/recommends")
@login_required_html
def my_recommends():
    recommends = find_my_recommends()
    return render_template("my_recommends.html", recommends=recommends)