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
                jsonify({"errors": {"email": f"{email} invalid"}}),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "message": f"email is valid {email!r}",
                    }
                ),
                200,
            )
