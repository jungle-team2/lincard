from flask import Blueprint, g, request, jsonify
from pymongo.errors import PyMongoError
from bson import SON, ObjectId

from db import db

from middlewares.auth_required import login_required


user_api = Blueprint("user", __name__)


def update_user(email, user):
    try:
        result = db.users.update_one({"email": email}, {"$set": user})
        print(result)
    except PyMongoError as e:
        print("update erorr:", e)
        raise RuntimeError("db update failed")
    if result.matched_count == 0:
        raise ValueError("not matched id")
    return result


@user_api.put("/my/recommends")
@login_required
def update_my_recommends():
    user = g.user
    user_id = user.get("_id")
    recommends = request.get_json()

    if not user_id:
        return jsonify({"error": "올바르지 않은 유저"}), 500

    db.recommends.delete_many({"userId": ObjectId(user_id)})

    for recommend in recommends:
        recommend["userId"] = ObjectId(user_id)
        db.recommends.insert_one(recommend)
    return jsonify({"result": "success"}), 200


@user_api.put("/my")
@login_required
def update_my():
    user = g.user
    body = request.get_json()
    data = body.get("data")
    ordered_data = SON(data)  # 순서 유지
    introduction = body.get("introduction")
    name = body.get("name")
    avatar_id = body.get("avatarId")

    try:
        update_user(
            user["email"],
            {
                "data": ordered_data,
                "introduction": introduction,
                "name": name,
                "avatarId": avatar_id,
            },
        )
    except ValueError as e:
        return jsonify({"result": "failed", "error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"result": "failed", "error": str(e)}), 500

    return jsonify({"result": "success"}), 200


@user_api.route("/<userId>/following", methods=["PATCH"])
@login_required
def following_api(userId):

    followerId = g.user["_id"]
    if not followerId:
        return jsonify({"result": "failed", "message": "올바르지 않은 유저"}), 400

    user = db.users.find_one({"_id": followerId, "followingIds": ObjectId(userId)})
    if user:
        return jsonify({"result": "failed", "message": "이미 팔로우한 유저입니다"}), 400

    db.users.update_one(
        {"_id": ObjectId(followerId)}, {"$addToSet": {"followingIds": ObjectId(userId)}}
    )

    return jsonify({"result": "success", "message": "성공적으로 팔로우"})


@user_api.route("/<userId>/following", methods=["DELETE"])
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
