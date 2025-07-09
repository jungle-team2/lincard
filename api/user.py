from flask import Blueprint, g, request, jsonify
from pymongo.errors import PyMongoError
from bson import SON

from db import db

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


@user_api.put("/my")
def update_my():
    user = g.user

    body = request.get_json()
    data = body.get("data")
    ordered_data = SON(data)  # 순서 유지
    introduction = body.get("introduction")

    try:
        update_user(
            user["email"],
            {
                "data": ordered_data,
                "introduction": introduction,
            },
        )
    except ValueError as e:
        return jsonify({"result": "failed", "error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"result": "failed", "error": str(e)}), 500

    return jsonify({"result": "success"}), 200
