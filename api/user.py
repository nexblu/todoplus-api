from flask import Blueprint, jsonify, request
from database import UserDatabase
from utils import token_required

user_router = Blueprint("api user", __name__)
user_database = UserDatabase()


@user_router.put("/todoplus/v1/user/username")
@token_required()
async def update_username():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    new_username = data.get("new_username")
    try:
        await user_database.update(
            "username",
            username=username,
            password=password,
            new_username=new_username,
        )
    except:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success change username {username!r}",
                }
            ),
            201,
        )


@user_router.put("/todoplus/v1/user/password")
@token_required()
async def update_password():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    new_password = data.get("new_password")
    if password != confirm_password:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"password and confirm password are not the same",
                }
            ),
            400,
        )
    try:
        await user_database.update(
            "password",
            username=username,
            password=password,
            new_password=new_password,
        )
    except:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 200,
                    "message": f"success change password {username!r}",
                }
            ),
            200,
        )
