from utils import UserNotFound, Validator
from config import access_token_key, algorithm, refresh_token_key
import jwt
import datetime
from database import UserCRUD
from flask_bcrypt import Bcrypt
from flask import jsonify


class LoginController:
    def __init__(self) -> None:
        self.user_database = UserCRUD()
        self.bcrypt = Bcrypt()

    async def login(self, username, password):
        if errors := await Validator.validate_login(username, password):
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": errors,
                        "data": {"username": username, "password": password},
                    }
                ),
                400,
            )
        try:
            user = await self.user_database.get("username", username=username)
        except UserNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"user {username} not found",
                        "data": {"username": username, "password": password},
                    }
                ),
                404,
            )
        else:
            try:
                if self.bcrypt.check_password_hash(user.password, password):
                    access_token = jwt.encode(
                        {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "is_active": user.is_active,
                            "is_admin": user.is_admin,
                            "exp": datetime.datetime.now(
                                datetime.timezone.utc
                            ).timestamp()
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
                            "exp": datetime.datetime.now(
                                datetime.timezone.utc
                            ).timestamp()
                            + datetime.timedelta(days=25).total_seconds(),
                        },
                        refresh_token_key,
                        algorithm=algorithm,
                    )
                    return (
                        jsonify(
                            {
                                "success": True,
                                "status_code": 200,
                                "message": f"user {user.username!r} was found",
                                "data": {
                                    "user_id": user.id,
                                    "username": user.username,
                                    "email": user.email,
                                    "password": password,
                                    "token": {
                                        "access_token": access_token,
                                        "refresh_token": refresh_token,
                                    },
                                },
                            }
                        ),
                        200,
                    )
                return (
                    jsonify(
                        {
                            "success": False,
                            "status_code": 404,
                            "message": f"user {username!r} not found",
                            "data": {"username": username, "password": password},
                        }
                    ),
                    404,
                )
            except TypeError:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status_code": 404,
                            "message": f"user {username!r} not found",
                            "data": {"username": username, "password": password},
                        }
                    ),
                    404,
                )
