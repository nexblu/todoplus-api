from .config import db_session, init_db
from models import User
from sqlalchemy import and_, func, or_
from .database import Database
import datetime


class UserDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")
        user = User(username, email, password)
        db_session.add(user)
        db_session.commit()

    async def get(self, type, **kwargs):
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")
        if type == "email":
            return User.query.filter(func.lower(User.email) == email.lower()).first()
        elif type == "username":
            return User.query.filter(
                func.lower(User.username) == username.lower()
            ).first()
        elif type == "login":
            return User.query.filter(
                and_(
                    func.lower(User.username) == username.lower(),
                    User.password == password,
                )
            ).first()
        elif type == "register":
            return User.query.filter(
                or_(
                    func.lower(User.username) == username.lower(),
                    func.lower(User.email) == email.lower(),
                )
            ).first()

    async def update(self, type, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email")
        is_active = kwargs.get("is_active")
        new_password = kwargs.get("new_password")
        new_username = kwargs.get("new_username")
        if type == "password":
            user = User.query.filter(
                and_(
                    func.lower(User.username) == username.lower(),
                    User.password == password,
                )
            ).first()
            user.password = new_password
            db_session.commit()
        elif type == "username":
            user = User.query.filter(
                and_(
                    func.lower(User.username) == username.lower(),
                    User.password == password,
                )
            ).first()
            user.username = new_username
            db_session.commit()
        elif type == "is_active":
            user = User.query.filter(
                and_(
                    func.lower(User.username) == username.lower(),
                    func.lower(User.email) == email.lower(),
                )
            ).first()
            user.is_active = is_active
            user.update_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            db_session.commit()

    async def delete(self):
        pass
