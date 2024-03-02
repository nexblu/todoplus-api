from flask import Blueprint, request, jsonify
from databases import add_user

register_router = Blueprint("api user register", __name__)


@register_router.post("/todoplus/v1/register")
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if username and email and password:
        add_user(username, email, password)
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": "success created",
                }
            ),
            201,
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
