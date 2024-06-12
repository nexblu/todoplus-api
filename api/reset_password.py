from flask import Blueprint, render_template, request, jsonify, redirect
from utils import TokenResetPassword
import smtplib
from email.mime.text import MIMEText
from config import (
    smtp_password,
    smtp_email,
    smtp_server,
    smtp_port,
    api_url,
    todoplus_url,
)
from repository import UserDatabase, ResetPasswordDatabase
from sqlalchemy import exc
import model

reset_router = Blueprint("route reset password", __name__)
user_database = UserDatabase()
token_database = ResetPasswordDatabase()


@reset_router.route(
    "/todoplus/v1/user/reset/reset-password/<string:token>", methods=["POST", "GET"]
)
async def reset_password(token):
    valid_token = await TokenResetPassword.get(token)
    if request.method == "POST":
        user_change_password = await user_database.get(
            "email", email=valid_token["email"]
        )
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        password_error = ""
        confirm_password_error = ""
        if not password.strip():
            password_error = "password is required"
        if not confirm_password.strip():
            confirm_password_error = "confirm password is required"
        if password.strip() != confirm_password.strip():
            password_error = "password do not match"
            confirm_password_error = "password do not match"
        if not password_error and not confirm_password_error:
            await user_database.update(
                "password",
                username=user_change_password.username,
                password=user_change_password.password,
                new_password=password.strip(),
            )
            await token_database.delete("email", email=user_change_password.email)
            return redirect(todoplus_url)
        return render_template(
            "forgot-password.html",
            password_error=password_error,
            confirm_password_error=confirm_password_error,
        )
    if valid_token:
        user_token_database = await token_database.get(
            "token", email=valid_token["email"], token=token
        )
        if user_token_database:
            return render_template("forgot-password.html")
        try:
            await token_database.delete("email", email=valid_token["email"])
        except:
            pass
    return "Invalid token"


@reset_router.post("/todoplus/v1/user/reset/email-reset-password")
async def email_reset_password():
    data = request.json
    email = data.get("email")
    token = await TokenResetPassword.insert(email)
    try:
        await token_database.insert(email, token)
    except exc.IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"failed send email to {email!r}",
                }
            ),
            400,
        )
    except model.reset_password.EmailRequired:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"data is invalid",
                }
            ),
            400,
        )
    except Exception:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"bad request",
                }
            ),
            400,
        )
    else:
        msg = MIMEText(
            f"""<h1>Hi, Welcome {email}</h1>

<p>Di Sini Kami Telah Mengirimkan Anda Untuk Merubah Password Anda: </p>
<a href={api_url}/todoplus/v1/user/reset/reset-password/{token}>Click Ini Untuk Reset Password</a>
""",
            "html",
        )
        msg["Subject"] = "Reset Password"
        msg["From"] = smtp_email
        msg["To"] = email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.send_message(msg)
                server.quit()
        except:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"failed send email to {email!r}",
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success send email to {email!r}",
                    }
                ),
                201,
            )
