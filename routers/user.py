from flask import Blueprint, jsonify, request
from databases import UserDatabase

user_router = Blueprint("api user", __name__)
db = UserDatabase()


@user_router.put("/todoplus/v1/user/username")
async def update_username():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    new_username = data.get("new_username")
    result = await db.get("login", username=username, password=password)
    if result:
        await db.update(
            "password",
            username=result.username,
            password=result.password,
            new_username=new_username,
        )
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": f"success change username {username!r}",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"user {username!r} not found",
                }
            ),
            404,
        )


@user_router.put("/todoplus/v1/user/password")
async def update_password():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    new_password = data.get("new_password")
    result = await db.get("login", username=username, password=password)
    if result:
        await db.update(
            "password",
            username=result.username,
            password=result.password,
            new_password=new_password,
        )
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": f"success change password {username!r}",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"user {username!r} not found",
                }
            ),
            404,
        )
