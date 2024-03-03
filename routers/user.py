from flask import Blueprint, jsonify, request
from databases import UserDatabase

user_router = Blueprint("api user", __name__)
db = UserDatabase()


@user_router.put("/todoplus/v1/user/change_password")
async def update_password():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    new_password = data.get("new_password")
    if username and password and new_password:
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
                        "result": "success change password",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "result": "bad request",
                    }
                ),
                400,
            )
    else:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": "bad request",
                }
            ),
            400,
        )
