from flask import jsonify
from email_validator import validate_email, EmailNotValidError


class EmailController:
    @staticmethod
    async def email_validator(email):
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"{email!r} not valid",
                        "data": {"email": email},
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"{email!r} is valid",
                        "data": {"email": email},
                    }
                ),
                200,
            )
