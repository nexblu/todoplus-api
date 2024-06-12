from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from repository import UserCRUD
from sqlalchemy.exc import IntegrityError
from utils import EmailNotValid

register_router = Blueprint("api user register", __name__)
bcrypt = Bcrypt()
user_database = UserCRUD()


@register_router.post("/todoplus/v1/user/register")
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
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        await user_database.insert(
            username=username,
            email=email,
            password=hashed_password,
        )
    except (IntegrityError, ValueError):
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"failed register",
                }
            ),
            400,
        )
    except EmailNotValid:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": "email not valid",
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
