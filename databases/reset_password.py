from .config import db_session, init_db
from models import ResetPassword
from .database import Database
from sqlalchemy import func, and_
import datetime


class ResetPasswordDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, email, token):
        reset_password = ResetPassword(email, token)
        db_session.add(reset_password)
        db_session.commit()

    async def delete(self, type, **kwargs):
        email = kwargs.get("email")
        if type == "email":
            user_token = ResetPassword.query.filter(
                func.lower(ResetPassword.email) == email.lower()
            ).first()
            db_session.delete(user_token)
            db_session.commit()

    async def get(self, type, **kwargs):
        email = kwargs.get("email")
        token = kwargs.get("token")
        if type == "email":
            return (
                ResetPassword.query.filter(
                    func.lower(ResetPassword.email) == email.lower()
                )
                .order_by(ResetPassword.created_at)
                .first()
            )
        elif type == "token":
            return ResetPassword.query.filter(
                and_(
                    func.lower(ResetPassword.email) == email.lower(),
                    ResetPassword.token == token,
                    datetime.datetime.now(datetime.timezone.utc).timestamp()
                    < ResetPassword.expired_at,
                )
            ).first()

    async def update(self, type, **kwargs):
        pass
