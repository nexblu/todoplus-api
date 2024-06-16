from flask import jsonify
from flask_bcrypt import Bcrypt
from database import UserCRUD
from sqlalchemy.exc import IntegrityError
from utils import EmailNotValid, Validator


class RegisterController:
    def __init__(self) -> None:
        self.user_database = UserCRUD()
        self.bcrypt = Bcrypt()

    async def add_user(self, username, email, password, confirm_password):
        if errors := await Validator.validate_register(
            username, email, password, confirm_password
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": errors,
                        "data": {
                            "username": username,
                            "email": email,
                            "password": password,
                            "confirm_password": confirm_password,
                        },
                    }
                ),
                400,
            )
        try:
            hashed_password = self.bcrypt.generate_password_hash(password).decode(
                "utf-8"
            )
            await self.user_database.insert(
                username=username,
                email=email,
                password=hashed_password,
            )
        except IntegrityError:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {"email": f"failed to register {email!r}"},
                        "data": {
                            "username": username,
                            "email": email,
                            "password": password,
                            "confirm_password": confirm_password,
                        },
                    }
                ),
                400,
            )
        except EmailNotValid:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {"email": f"email not valid {email!r}"},
                        "data": {
                            "username": username,
                            "email": email,
                            "password": password,
                            "confirm_password": confirm_password,
                        },
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 201,
                        "message": {"email": f"successfully registered {email!r}"},
                        "data": {
                            "username": username,
                            "email": email,
                            "password": password,
                            "confirm_password": confirm_password,
                        },
                    }
                ),
                201,
            )
