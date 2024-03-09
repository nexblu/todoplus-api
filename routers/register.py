from flask import Blueprint, request, jsonify
from databases import UserDatabase

register_router = Blueprint("api user register", __name__)
db = UserDatabase()


@register_router.post("/todoplus/v1/register")
async def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    try:
        await db.insert(username=username, email=email, password=password)
    except:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": f"user {username!r} already available",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": "success created",
                }
            ),
            201,
        )
