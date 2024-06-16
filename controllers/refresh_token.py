from flask_bcrypt import Bcrypt
from flask import jsonify
import jwt
from config import refresh_token_key, access_token_key, algorithm
import datetime
from traceback import print_exc


class RefreshTokenController:
    def __init__(self) -> None:
        self.bcrypt = Bcrypt()

    async def refresh_token(self, token):
        if not token or token.isspace():
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {
                            "token": "token is empety",
                        },
                        "data": {"token": token},
                    }
                ),
                400,
            )
        try:
            decoded_token = jwt.decode(token, refresh_token_key, algorithms=algorithm)
        except:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"token invalid",
                        "data": {"token": token},
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
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 201,
                        "message": f"create new token",
                        "data": {
                            "token": {
                                "access_token": access_token,
                            }
                        },
                    }
                ),
                201,
            )
