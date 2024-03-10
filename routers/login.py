import jwt
from flask import Blueprint, jsonify
from databases import UserDatabase
from config import jwt_key, algorithm

login_router = Blueprint("api user login", __name__)
db = UserDatabase()


@login_router.get("/todoplus/v1/login/<string:username>/<string:password>")
async def login(username, password):
    try:
        result = await db.get("login", username=username, password=password)
    except:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"{username!r} not found",
                }
            ),
            404,
        )
    else:
        if result:
            encoded_jwt = jwt.encode(
                {
                    "username": result.username,
                    "email": result.email,
                    "password": result.password,
                },
                jwt_key,
                algorithm=algorithm,
            )
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "result": {"token": encoded_jwt},
                    }
                ),
                200,
            )
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": "bad request",
                }
            ),
            404,
        )
