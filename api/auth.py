from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    make_response,
)
from pymongo.errors import PyMongoError

import bcrypt
import re
import bcrypt
from datetime import datetime, timedelta
from utils.jwt_utils import encode

# settings
from db import db

users = db["users"]

auth_api = Blueprint("auth", __name__)


# utils
def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password, hashed) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_jwt(email):
    payload = {"email": email, "exp": datetime.utcnow() + timedelta(hours=1)}
    return encode(payload)


def validation_signup(form_data) -> str | None:
    if not form_data["email"] or not form_data["password"]:
        return "모든 정보를 입력해주세요"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", form_data["email"]):
        return "올바른 이메일 형식이 아닙니다"

    pattern = (
        r'^(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'
    )
    if not re.match(pattern, form_data["password"]):
        return "비밀번호는 8자 이상, 숫자, 특수문자를 모두 포함해야 합니다."

    if form_data["password"] != form_data["pwdchk"]:
        return "패스워드가 일치하지 않습니다"

    return None


@auth_api.post("/login")
def login():
    form_data = {
        "email": request.form.get("email"),
        "password": request.form.get("password"),
    }

    if not form_data["email"] or not form_data["password"]:
        return render_template(
            "login.html", error="이메일 혹은 패스워드가 잘못되었습니다", form=form_data
        )

    user = users.find_one({"email": form_data["email"]})
    if not user:
        return render_template(
            "login.html", error="이메일 혹은 패스워드가 잘못되었습니다", form=form_data
        )

    if not verify_password(form_data["password"], user.get("password")):
        return render_template(
            "login.html", error="이메일 혹은 패스워드가 잘못되었습니다", form=form_data
        )

    token = create_jwt(form_data["email"])

    resp = make_response(redirect("/"))
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        # secure=False,
        samesite="Lax",
        max_age=3600,
    )
    return resp


@auth_api.post("/sign-up")
def sign_up():
    form_data = {
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "pwdchk": request.form.get("pwdchk"),
    }

    error = validation_signup(form_data)
    if error:
        return render_template("signup.html", error=error, form=form_data)

    if users.find_one({"email": form_data["email"]}):
        return render_template(
            "signup.html", error="이미 가입된 이메일입니다.", form=form_data
        )

    hashed_password = get_password_hash(form_data["password"])

    new_user = {
        "email": form_data["email"],
        "password": hashed_password,
        "binaryUrl": "",
        "avatarId": 1,
        "name": form_data["email"].split(sep="@")[0],
        "introduction": "",
        # "introduction": "안녕 테스트",
        "data": {},
    }

    try:
        users.insert_one(new_user)
    except PyMongoError as e:
        return render_template(
            "signup.html", error="회원가입 중 오류가 발생했습니다.", form=form_data
        )

    return redirect(url_for("main.login"))


@auth_api.post("/logout")
def logout():
    resp = make_response(redirect("/"))

    resp.set_cookie(
        "access_token",  # 쿠키 이름
        "",  # 빈 값으로 설정
        max_age=0,  # 즉시 만료
        httponly=True,  # 보안 설정 유지
        secure=True,  # HTTPS 환경이라면 True
        samesite="Lax",  # 또는 'Strict' or 'None'
        path="/",  # 해당 경로 전체에서 쿠키 제거
    )

    resp.set_cookie(
        "recent_users",  # 쿠키 이름
        "",  # 빈 값으로 설정
        max_age=0,  # 즉시 만료
        httponly=True,  # 보안 설정 유지
        secure=True,  # HTTPS 환경이라면 True
        samesite="Lax",  # 또는 'Strict' or 'None'
        path="/",  # 해당 경로 전체에서 쿠키 제거
    )

    return resp
