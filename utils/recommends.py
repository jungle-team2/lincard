from flask import g
from db import db
from bson import ObjectId

from middlewares.auth_required import login_required

from pymongo.errors import PyMongoError


@login_required
def find_my_recommends():
    return find_recommends(g.user)


def find_recommends(user, user_id=None):
    user_id = user_id if user_id else user.get("_id")
    if user_id:
        try:
            recommends = list(db.recommends.find({"userId": ObjectId(user_id)}))
            print(len(recommends))
            return recommends
        except KeyError as e:
            raise KeyError("올바르지 않은 user 데이터")
        except PyMongoError as e:
            raise RuntimeError("find 중 에러")
    else:
        return []
