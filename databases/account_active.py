from .config import db_session, init_db
from models import AccountActive
from .database import Database
from sqlalchemy import func, and_


class AccountActiveDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, email, token):
        reset_password = AccountActive(email, token)
        db_session.add(reset_password)
        db_session.commit()

    async def delete(self, type, **kwargs):
        email = kwargs.get("email")
        if type == "email":
            user_token = AccountActive.query.filter(
                func.lower(AccountActive.email) == email.lower()
            ).first()
            db_session.delete(user_token)
            db_session.commit()

    async def get(self, type, **kwargs):
        email = kwargs.get("email")
        token = kwargs.get("token")
        if type == "email":
            return (
                AccountActive.query.filter(
                    func.lower(AccountActive.email) == email.lower()
                )
                .order_by(AccountActive.created_at)
                .first()
            )
        elif type == "token":
            return AccountActive.query.filter(
                and_(
                    func.lower(AccountActive.email) == email.lower(),
                    AccountActive.token == token,
                )
            ).first()

    async def update(self, type, **kwargs):
        pass
