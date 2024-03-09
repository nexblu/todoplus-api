from flask import Blueprint, jsonify
from email_validator import validate_email, EmailNotValidError

email_router = Blueprint("api email", __name__)


@email_router.get("/todoplus/v1/email/<string:email>")
async def email_validator(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
    except EmailNotValidError as e:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"email {email!r} not valid",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": "email is valid",
                }
            ),
            200,
        )
