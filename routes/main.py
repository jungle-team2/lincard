from flask import (
    Blueprint,
    render_template,
    g,
    request,
    make_response,
    jsonify,
    redirect,
    url_for,
    flash,
)
from middlewares.auth_required import login_required_html
from typing import List, Dict
from dto.users import ProfileDTO
from utils.recommends import find_recommends, find_my_recommends
from bson import ObjectId
import json

main = Blueprint("main", __name__, template_folder="templates")

from db import db

usersCollection = db["users"]


@main.route("/")
def index():
    recent_raw = request.cookies.get("recent_users", "[]")
    try:
        recent_ids = json.loads(recent_raw)
    except:
        recent_ids = []
    if not recent_ids:
        return swip()

    recent = db.users.find_one({"_id": ObjectId(recent_ids[-1])})
    recommends = find_recommends(recent)
    return render_template("index.html", feed=recent, recommends=recommends)


@main.route("/swip")
def swip():
    recent_raw = request.cookies.get("recent_users", "[]")
    try:
        exclude_ids = json.loads(recent_raw)
    except:
        exclude_ids = []

    pipeline = get_random_user_pipeline(exclude_ids)
    random_user = list(usersCollection.aggregate(pipeline))

    # if not random_user:,
    #     return render_template("index.html", feed=None) 없을경우 어떻게 처리할건지 논의

    random_user = random_user[0] if random_user else None
    if random_user is None:
        return render_template("index.html", error="모든 유저를 탐색했습니다")

    feed = ProfileDTO(
        userId=str(random_user["_id"]),
        email=random_user["email"],
        introduction=random_user["introduction"],
        data=random_user["data"],
        name=random_user["name"],
        avatarId=random_user["avatarId"],
    )

    if feed.userId in exclude_ids:
        exclude_ids.remove(feed.userId)
    exclude_ids.append(feed.userId)

    resp = make_response(redirect(url_for("main.index")))
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


@main.route("/<userId>/following", methods=["PATCH"])
@login_required_html
def following(userId):

    followerId = g.user["_id"]
    if not followerId:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400

    db.users.update_one(
        {"_id": ObjectId(followerId)}, {"$addToSet": {"followingIds": ObjectId(userId)}}
    )

    return jsonify({"result": "success", "message": "성공적으로 팔로윙"})

@main.route("/<userId>/following", methods=["DELETE"])
@login_required_html
def un_following(userId):

    followerId = g.user["_id"]
    if not followerId:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400
    
    if not ObjectId.is_valid(userId):
        return jsonify({"result": "failed", "message": "올바르지 않은 사용자 ID"}), 400

    result = db.users.update_one(
        {"_id": ObjectId(followerId)}, 
        {"$pull": {"followingIds": ObjectId(userId)}}
    )
    
    if result.modified_count == 0:
        return jsonify({"result": "failed", "message": "팔로우하지 않은 사용자입니다"}), 400
    
    return jsonify({"result": "success", "message": "성공적으로 언팔로우했습니다."})




@main.route("/<userId>/recommends", methods=["GET"])
@login_required_html
def get_recommends(userId):
    recommends = find_recommends(None, userId)
    recommendDTOs = []
    try:
        recommendDTOs = [
            {
                "title": rec["title"],
                "url": rec["url"],
                "description": rec["description"],
            }
            for rec in recommends
        ]
    except:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400

    return jsonify({"result": "success", "recommends": recommendDTOs}), 200


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
