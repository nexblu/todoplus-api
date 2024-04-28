from databases import AccountActiveDatabase, UserDatabase
from flask import Blueprint, jsonify, request, render_template
from utils import AccountActive
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
from sqlalchemy import exc
import models

account_active_router = Blueprint("api account active", __name__)
account_active_database = AccountActiveDatabase()
user_database = UserDatabase()


@account_active_router.get("/todoplus/v1/user/email-verify/<string:token>")
async def account_active(token):
    if valid_token := await AccountActive.get(token):
        if user_token_database := await account_active_database.get(
            "token", email=valid_token["email"], token=token
        ):
            if (
                datetime.datetime.now(datetime.timezone.utc).timestamp()
                <= user_token_database.expired_at
            ):
                try:
                    await user_database.update(
                        "is_active",
                        is_active=True,
                        email=user_token_database.email,
                    )
                except:
                    return "invalid token"
                else:
                    await account_active_database.delete(
                        "email", email=user_token_database.email
                    )
                    return render_template("account-active.html", url=todoplus_url)
        try:
            await account_active_database.delete("email", email=valid_token["email"])
        except:
            pass
    return "invalid token"


@account_active_router.post("/todoplus/v1/user/email-verify")
async def account_active_email():
    data = request.json
    email = data.get("email")
    token = await AccountActive.insert(email)
    try:
        await account_active_database.insert(email, token)
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
    except models.account_active.EmailRequired:
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
                        "status_code": 400,
                        "result": f"failed send email to {email!r}",
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "result": f"success send email to {email!r}",
                    }
                ),
                201,
            )
