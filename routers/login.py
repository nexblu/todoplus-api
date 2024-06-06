from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from databases import UserCRUD
from utils import UserNotFound
from config import access_token_key, algorithm, refresh_token_key
import jwt
import datetime

login_router = Blueprint("api user login", __name__)
bcrypt = Bcrypt()
user_database = UserCRUD()


@login_router.post("/todoplus/v1/user/login")
async def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    try:
        user = await user_database.get("email", email=email)
    except UserNotFound:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {email!r} not found",
                }
            ),
            404,
        )
    else:
        if bcrypt.check_password_hash(user.password, password):
            access_token = jwt.encode(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(minutes=5).total_seconds(),
                },
                access_token_key,
                algorithm=algorithm,
            )
            refresh_token = jwt.encode(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(days=25).total_seconds(),
                },
                refresh_token_key,
                algorithm=algorithm,
            )
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "result": {
                            "token": {
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                            }
                        },
                        "message": f"user {email!r} was found",
                    }
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": None,
                    "message": f"user {email!r} not found",
                }
            ),
            404,
        )
