from sqlalchemy import Table, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime
import re

mapper_registry = registry()


def check_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[!@#$%^&*()-+=]", password):
        return False
    return True


class UsernameRequired(Exception):
    def __init__(self, message="username is required"):
        self.message = message
        super().__init__(self.message)


class EmailRequired(Exception):
    def __init__(self, message="email is required"):
        self.message = message
        super().__init__(self.message)


class PasswordInvalid(Exception):
    def __init__(self, message="password invalid"):
        self.message = message
        super().__init__(self.message)


class User:
    query = db_session.query_property()

    def __init__(self, username, email, password):
        if username_space := username.isspace() or not username:
            raise UsernameRequired
        else:
            self.username = username
        if email_space := email.isspace() or not email:
            raise EmailRequired
        else:
            self.email = email
        if (
            password_valid := check_password_strength(password)
            or not (password_space := password.isspace())
            or password
        ):
            self.password = password
        else:
            raise PasswordInvalid

    def __repr__(self):
        return f"<User {self.username!r}>"


user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="C"), unique=True, nullable=False),
    Column("email", String(collation="C"), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column(
        "update_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column(
        "created_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column("is_active", Boolean, default=False),
)

mapper_registry.map_imperatively(User, user_table)
