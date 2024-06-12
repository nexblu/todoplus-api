from utils import UserNotFound
from config import access_token_key, algorithm, refresh_token_key
import jwt
import datetime
from repository import UserCRUD
from flask_bcrypt import Bcrypt
from flask import jsonify


class LoginService(UserCRUD, Bcrypt):
    def __init__(self) -> None:
        pass

    async def login(self, email, password):
        try:
            user = await self.get("email", email=email)
        except UserNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"user {email!r} not found",
                    }
                ),
                404,
            )
        else:
            try:
                if self.check_password_hash(user.password, password):
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
                                "status_code": 200,
                                "result": {
                                    "token": {
                                        "access_token": access_token,
                                        "refresh_token": refresh_token,
                                    }
                                },
                                "message": f"user {email!r} was found",
                            }
                        ),
                        200,
                    )
                return (
                    jsonify(
                        {
                            "status_code": 404,
                            "result": None,
                            "message": f"user {email!r} not found",
                        }
                    ),
                    404,
                )
            except TypeError:
                return (
                    jsonify(
                        {
                            "status_code": 404,
                            "result": None,
                            "message": f"user {email!r} not found",
                        }
                    ),
                    404,
                )
