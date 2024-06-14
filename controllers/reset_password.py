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
from database import UserCRUD, ResetPasswordCRUD
from sqlalchemy.exc import IntegrityError
import models


class ResetPasswordController:
    def __init__(self) -> None:
        self.user_database = UserCRUD()
        self.token_database = ResetPasswordCRUD()

    async def get_reset_password(self, token):
        valid_token = await TokenResetPassword.get(token)
        if request.method == "POST":
            user_change_password = await self.user_database.get(
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
                await self.user_database.update(
                    "password",
                    username=user_change_password.username,
                    password=user_change_password.password,
                    new_password=password.strip(),
                )
                await self.token_database.delete(
                    "email", email=user_change_password.email
                )
                return redirect(todoplus_url)
            return render_template(
                "forgot-password.html",
                password_error=password_error,
                confirm_password_error=confirm_password_error,
            )
        if valid_token:
            user_token_database = await self.token_database.get(
                "token", email=valid_token["email"], token=token
            )
            if user_token_database:
                return render_template("forgot-password.html")
            try:
                await self.token_database.delete("email", email=valid_token["email"])
            except:
                pass
        return "Invalid token"

    async def reset_password(self, email):
        if not email or email.isspace():
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {"email": "email is empety"},
                        "data": {"email": email},
                    }
                ),
                400,
            )
        token = await TokenResetPassword.insert(email)
        try:
            user = await self.token_database.insert(email, token)
        except IntegrityError:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"link reset password already send to {email!r}",
                        "data": {"email": email},
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
                            "success": False,
                            "status_code": 400,
                            "message": {"SMPTP": f"failed send email to {email!r}"},
                            "data": {
                                "user_id": user.id,
                                "username": user.username,
                                "email": user.email,
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
                            "message": f"success send link reset password to {email!r}",
                            "data": {
                                "email": email,
                                "user_id": user.id,
                                "username": user.username,
                                "link": f"{api_url}/todoplus/v1/user/reset/reset-password/{token}",
                            },
                        }
                    ),
                    201,
                )
