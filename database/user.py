from .config import db_session, init_db
from models import UserDatabase
from sqlalchemy import and_, func, or_
from .database import Database
import datetime
from utils import UserNotFound


class UserCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        user = UserDatabase(username, email, password, created_at, created_at)
        db_session.add(user)
        db_session.commit()

    async def get(self, type, **kwargs):
        email = kwargs.get("email")
        if type == "email":
            try:
                if user := UserDatabase.query.filter(
                    func.lower(UserDatabase.email) == email.lower()
                ).first():
                    return user
                raise UserNotFound
            except:
                raise UserNotFound

    async def update(self, category, **kwargs):
        is_active = kwargs.get("is_active")
        updated_at = kwargs.get("updated_at")
        user_id = kwargs.get("user_id")
        email = kwargs.get("email")
        if category == "is_active":
            if user := UserDatabase.query.filter(
                func.lower(UserDatabase.email) == email.lower()
            ).first():
                user.is_active = is_active
                user.updated_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
                return
            raise UserNotFound
        elif category == "updated_at":
            if user := UserDatabase.query.filter(UserDatabase.id == user_id).first():
                user.updated_at = updated_at
                db_session.commit()
                return
            raise UserNotFound

    async def delete(self, category, **kwargs):
        pass
