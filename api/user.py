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
    try:
        update_user(
            user["email"],
            {
                "data": ordered_data,
                "introduction": introduction,
                "name": name,
            },
        )
    except ValueError as e:
        return jsonify({"result": "failed", "error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"result": "failed", "error": str(e)}), 500

    return jsonify({"result": "success"}), 200
