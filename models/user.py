from sqlalchemy import Table, Column, Integer, String, Boolean, Float, CheckConstraint
from sqlalchemy.orm import registry
from databases import metadata, db_session
import re
from utils import PasswordNotSecure, EmailNotValid
from email_validator import validate_email, EmailNotValidError

mapper_registry = registry()


class UserDatabase:
    query = db_session.query_property()

    def __init__(self, username, email, password):
        self.username = username
        self.email = self.validate_email(email)
        self.password = self.check_password_strength(password)

    def __repr__(self):
        return f"<User {self.username!r}>"

    @staticmethod
    def check_password_strength(password):
        if len(password) < 8:
            raise PasswordNotSecure
        if not re.search(r"\d", password):
            raise PasswordNotSecure
        if not re.search(r"[A-Z]", password):
            raise PasswordNotSecure
        if not re.search(r"[a-z]", password):
            raise PasswordNotSecure
        if not re.search(r"[!@#$%^&*()-+=]", password):
            raise PasswordNotSecure
        return password

    @staticmethod
    def validate_email(email):
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            raise EmailNotValid
        return email


user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="C"), unique=True, nullable=False),
    Column("email", String(collation="C"), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("is_active", Boolean, default=False),
    CheckConstraint("length(username) > 0", name="non_empty_username"),
    CheckConstraint("length(email) > 0", name="non_empty_email"),
    CheckConstraint("length(password) > 0", name="non_empty_password"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
)

mapper_registry.map_imperatively(UserDatabase, user_table)
