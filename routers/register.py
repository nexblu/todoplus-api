from flask import Blueprint, request, jsonify
from databases import UserDatabase
from sqlalchemy import exc
import models

register_router = Blueprint("api user register", __name__)
user_database = UserDatabase()


@register_router.post("/todoplus/v1/register")
async def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
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
        await user_database.insert(username=username, email=email, password=password)
    except (
        models.user.EmailRequired,
        models.user.UsernameRequired,
    ):
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": "data is invalid",
                }
            ),
            400,
        )
    except models.user.PasswordInvalid:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": "password not secure",
                }
            ),
            400,
        )
    except exc.IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"failed register {username!r}",
                }
            ),
            400,
        )
    except Exception:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": "bad request",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success register {username!r}",
                }
            ),
            201,
        )
