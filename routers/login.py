import jwt
from flask import Blueprint, jsonify
from databases import UserDatabase
from config import jwt_key, algorithm

login_router = Blueprint("api user login", __name__)
user_database = UserDatabase()


@login_router.get("/todoplus/v1/login/<string:username>/<string:password>")
async def login(username, password):
    if user_login := await user_database.get(
        "login", username=username, password=password
    ):
        encoded_jwt = jwt.encode(
            {
                "username": user_login.username,
                "email": user_login.email,
                "password": user_login.password,
                "is_active": user_login.is_active,
            },
            jwt_key,
            algorithm=algorithm,
        )
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": {"token": encoded_jwt},
                    "message": f"user {username!r} was found",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
