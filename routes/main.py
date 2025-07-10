from flask import (
    Blueprint,
    render_template,
    g,
    request,
    make_response,
    jsonify,
    redirect,
    url_for,
)
from middlewares.auth_required import login_required_html, login_required
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
    # 추가 유사 판정
    if getattr(g, "user", None):
        my_rec = find_my_recommends()
        my_urls = {r["url"] for r in my_rec}
        some_same_rec = any(r["url"] in my_urls for r in recommends)
    else:
        some_same_rec = False

    recent["hasSameRecommend"] = some_same_rec
    return render_template("index.html", feed=recent, recommends=recommends)


@main.route("/swip")
def swip():
    filter_option = request.args.get("filter")
    recent_raw = request.cookies.get("recent_users", "[]")

    if getattr(g, "user", None) and filter_option == "same-recommend":
        my_rec = find_my_recommends()
        my_urls = list({r["url"] for r in my_rec})
    else:
        my_urls = []

    try:
        exclude_ids = json.loads(recent_raw)
    except:
        exclude_ids = []
    # 본인제외
    if getattr(g, "user", None):
        exclude_ids.append(str(g.user["_id"]))

    pipeline = get_random_user_pipeline(exclude_ids, my_urls)
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
        "recent_users", json.dumps(exclude_ids[-5:]), max_age=86400, path="/"
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


# user api


@main.route("/<userId>/following", methods=["PATCH"])
@login_required
def following(userId):

    followerId = g.user["_id"]
    if not followerId:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400

    db.users.update_one(
        {"_id": ObjectId(followerId)}, {"$addToSet": {"followingIds": ObjectId(userId)}}
    )

    return jsonify({"result": "success", "message": "성공적으로 팔로윙"})


@main.route("/<userId>/following", methods=["DELETE"])
@login_required
def un_following(userId):

    followerId = g.user["_id"]
    if not followerId:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400

    if not ObjectId.is_valid(userId):
        return jsonify({"result": "failed", "message": "올바르지 않은 사용자 ID"}), 400

    result = db.users.update_one(
        {"_id": ObjectId(followerId)}, {"$pull": {"followingIds": ObjectId(userId)}}
    )

    if result.modified_count == 0:
        return (
            jsonify({"result": "failed", "message": "팔로우하지 않은 사용자입니다"}),
            400,
        )

    return jsonify({"result": "success", "message": "성공적으로 언팔로우했습니다."})


@main.route("/<userId>/recommends", methods=["GET"])
@login_required
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


def get_random_user_pipeline(
    ignore_ids: List[str], recommended_urls: List[str]
) -> List[Dict[str, any]]:
    oids = []
    for id in ignore_ids:
        oids.append(ObjectId(id))

    pipeline = [
        {"$match": {"_id": {"$nin": oids}}},
        {
            "$lookup": {
                "from": "recommends",
                "localField": "_id",
                "foreignField": "userId",
                "as": "user_recommends",
            }
        },
    ]
    if recommended_urls:
        pipeline.append({"$match": {"user_recommends.url": {"$in": recommended_urls}}})

    pipeline.append({"$sample": {"size": 1}})
    return pipeline


@main.route("/mypage/recommends")
@login_required_html
def my_recommends():
    recommends = find_my_recommends()
    return render_template("my_recommends.html", recommends=recommends)
