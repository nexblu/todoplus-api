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
            if user := UserDatabase.query.filter(
                func.lower(UserDatabase.email) == email.lower()
            ).first():
                return user
            raise UserNotFound

    async def update(self, type, **kwargs):
        pass

    async def delete(self):
        pass
