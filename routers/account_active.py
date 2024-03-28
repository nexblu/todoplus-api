from databases import AccountActiveDatabase, UserDatabase
from flask import Blueprint, jsonify, request, render_template
from utils import AccountActiveToken
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

account_active_router = Blueprint("api account active", __name__)
db_account_active = AccountActiveDatabase()
db_user = UserDatabase()


@account_active_router.get("/todoplus/v1/user/email-verify/<string:token>")
async def account_active(token):
    token_ = await AccountActiveToken.verify_token(token)
    user = await db_user.get("email", email=token_["email"])
    user_token = await db_account_active.get(
        "token", email=token_["email"], token=token
    )
    if user and user_token:
        if (
            user.is_active == False
            and datetime.datetime.now(datetime.timezone.utc).timestamp()
            <= user_token.expired_at
        ):
            await db_user.update(
                "is_active", is_active=True, username=user.username, email=user.email
            )
            await db_account_active.delete("email", email=user.email)
            return render_template("account-active.html", url=todoplus_url)
    return "invalid token"


@account_active_router.post("/todoplus/v1/user/email-verify")
async def account_active_email():
    data = request.json
    email = data.get("email")
    token = await AccountActiveToken().get_token(email)
    user = await db_account_active.get("token", email=email, token=token)
    if not user:
        await db_account_active.insert(email, token)
    msg = MIMEText(
        f"""<h1>Hi, Welcome {email}</h1>

<p>Di Sini Kami Telah Mengirimkan Anda Untuk Merubah Password Anda: </p>
<a href={api_url}/todoplus/v1/user/email-verify/{token}>Click Ini Untuk Verify Email</a>
""",
        "html",
    )
    msg["Subject"] = "Verify Email"
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
