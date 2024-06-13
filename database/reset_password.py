from .config import db_session, init_db
from models import ResetPasswordDatabase
from .database import Database
from sqlalchemy import func, and_
import datetime


class ResetPasswordCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, email, token):
        reset_password = ResetPasswordDatabase(email, token)
        db_session.add(reset_password)
        db_session.commit()

    async def delete(self, type, **kwargs):
        email = kwargs.get("email")
        if type == "email":
            user_token = ResetPasswordDatabase.query.filter(
                func.lower(ResetPasswordDatabase.email) == email.lower()
            ).first()
            db_session.delete(user_token)
            db_session.commit()

    async def get(self, type, **kwargs):
        email = kwargs.get("email")
        token = kwargs.get("token")
        if type == "email":
            return (
                ResetPasswordDatabase.query.filter(
                    func.lower(ResetPasswordDatabase.email) == email.lower()
                )
                .order_by(ResetPasswordDatabase.created_at)
                .first()
            )
        elif type == "token":
            return ResetPasswordDatabase.query.filter(
                and_(
                    func.lower(ResetPasswordDatabase.email) == email.lower(),
                    ResetPasswordDatabase.token == token,
                    datetime.datetime.now(datetime.timezone.utc).timestamp()
                    < ResetPasswordDatabase.expired_at,
                )
            ).first()

    async def update(self, type, **kwargs):
        pass
