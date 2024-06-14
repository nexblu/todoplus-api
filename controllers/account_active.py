from database import AccountActiveCRUD, UserCRUD
from flask import jsonify, render_template
from utils import AccountActive, UserNotFound
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
import datetime
from sqlalchemy.exc import IntegrityError


class AccountActiveController:
    def __init__(self) -> None:
        self.account_active_database = AccountActiveCRUD()
        self.user_database = UserCRUD()

    async def email_verify(self, email):
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
        try:
            user = await self.user_database.get("email", email=email)
        except UserNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"user {email!r} not found",
                        "data": {"email": email},
                    }
                ),
                404,
            )
        else:
            if user.is_active:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status_code": 400,
                            "message": f"user {email!r} is active",
                            "data": {
                                "user_id": user.id,
                                "username": user.username,
                                "email": user.email,
                            },
                        }
                    ),
                    400,
                )
            created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            expired_at = created_at + (datetime.timedelta(hours=7).total_seconds())
            token = await AccountActive.insert(user.id, email)
            try:
                await self.account_active_database.insert(
                    user.id,
                    token,
                    created_at,
                    expired_at,
                )
            except IntegrityError:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status_code": 400,
                            "message": f"user {email!r} already get link account active",
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
                msg = MIMEText(
                    f"""<h1>Hi, Welcome {email}</h1>

    <p>Di Sini Kami Telah Mengirimkan Anda Untuk Verif Account: </p>
    <a href={api_url}/todoplus/v1/user/email-verify/{token}>Click Ini Untuk Verify Email</a>
    """,
                    "html",
                )
                msg["Subject"] = "Verify Email"
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
                                "message": f"success send link email active to {email!r}",
                                "data": {
                                    "email": email,
                                    "user_id": user.id,
                                    "username": user.username,
                                    "link": f"{api_url}/todoplus/v1/user/email-verify/{token}",
                                },
                            }
                        ),
                        201,
                    )

    async def get_account_active(self, token):
        if valid_token := await AccountActive.get(token):
            try:
                user_token_database = await self.account_active_database.get(
                    "token", user_id=valid_token["user_id"], token=token
                )
            except UserNotFound:
                await self.account_active_database.delete(
                    "user_id", user_id=valid_token["user_id"]
                )
                return render_template("not_found.html")
            else:
                try:
                    await self.user_database.update(
                        "is_active",
                        is_active=True,
                        email=valid_token["email"],
                    )
                except:
                    await self.account_active_database.delete(
                        "user_id", user_id=user_token_database.user_id
                    )
                    return render_template("not_found.html")
                else:
                    await self.account_active_database.delete(
                        "user_id", user_id=user_token_database.user_id
                    )
                    return render_template("email_active.html", url=todoplus_url)
        return render_template("not_found.html")
