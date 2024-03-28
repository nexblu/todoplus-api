from flask import Blueprint, render_template, request, jsonify, redirect
from utils import ResetPassword
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
from databases import UserDatabase, ResetPasswordDatabase

reset_router = Blueprint("route reset password", __name__)
db = UserDatabase()
token_db = ResetPasswordDatabase()


@reset_router.route(
    "/todoplus/v1/user/reset/reset-password/<string:token>", methods=["POST", "GET"]
)
async def reset_password(token):
    token_ = await ResetPassword.verify_reset_token(token)
    user = await db.get("email", email=token_["email"])
    if request.method == "POST":
        password_error = ""
        confirm_password_error = ""
        if (
            request.form["password"]
            and request.form["confirm_password"]
            and request.form["password"] == request.form["confirm_password"]
        ):
            user_token = await token_db.get("token", email=token_["email"], token=token)
            if user_token:
                await db.update(
                    "password",
                    username=user.username,
                    password=user.password,
                    new_password=request.form["password"],
                )
                await token_db.delete("email", email=token_["email"])
                return redirect(todoplus_url)
            else:
                return "invalid token"
        else:
            if not request.form["password"]:
                password_error = "Password Is Required."
            if not request.form["confirm_password"]:
                confirm_password_error = "Password Is Required."
            if request.form["password"] != request.form["confirm_password"]:
                password_error = "Password Does No Match."
                confirm_password_error = "Password Does No Match."
            return render_template(
                "forgot-password.html",
                password_error=password_error,
                confirm_password_error=confirm_password_error,
            )
    if token_:
        if user:
            user_token = await token_db.get("token", email=token_["email"], token=token)
            if user_token:
                return render_template(
                    "forgot-password.html",
                )
    return "token invalid"


@reset_router.post("/todoplus/v1/user/reset/email-reset-password")
async def email_reset_password():
    data = request.json
    email = data.get("email")
    token = await ResetPassword.get_reset_token(email)
    user = await token_db.get("token", email=email, token=token)
    if not user:
        await token_db.insert(email, token)
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

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": f"success send email",
                }
            ),
            200,
        )
