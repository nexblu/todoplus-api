from database import UserCRUD
from flask_bcrypt import Bcrypt
from flask import jsonify
import jwt
from config import refresh_token_key, access_token_key, algorithm
import datetime


class RefreshTokenController:
    def __init__(self) -> None:
        self.user_database = UserCRUD()
        self.bcrypt = Bcrypt()

    async def refresh_token(token):
        try:
            decoded_token = jwt.decode(
                refresh_token, refresh_token_key, algorithms=algorithm
            )
        except:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "result": None,
                        "message": f"token invalid",
                    }
                ),
                400,
            )
        else:
            access_token = jwt.encode(
                {
                    "user_id": decoded_token["user_id"],
                    "username": decoded_token["username"],
                    "email": decoded_token["email"],
                    "is_active": decoded_token["is_active"],
                    "is_admin": decoded_token["is_admin"],
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(minutes=5).total_seconds(),
                },
                access_token_key,
                algorithm=algorithm,
            )
            refresh_token = jwt.encode(
                {
                    "user_id": decoded_token["user_id"],
                    "username": decoded_token["username"],
                    "email": decoded_token["email"],
                    "is_active": decoded_token["is_active"],
                    "is_admin": decoded_token["is_admin"],
                    "exp": datetime.datetime.now(datetime.timezone.utc).timestamp()
                    + datetime.timedelta(days=25).total_seconds(),
                },
                refresh_token_key,
                algorithm=algorithm,
            )
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "result": {
                            "token": {
                                "access_token": access_token,
                                "refresh_token": refresh_token,
                            }
                        },
                        "message": f"token is valid",
                    }
                ),
                201,
            )
