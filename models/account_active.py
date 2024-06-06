from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session
from email_validator import validate_email, EmailNotValidError
from utils import EmailNotValid

mapper_registry = registry()


class AccountActive:
    query = db_session.query_property()

    def __init__(self, email, token):
        self.email = self.validate_email(email)
        self.token = token

    def __repr__(self):
        return f"<User {self.email!r}>"

    @staticmethod
    def validate_email(email):
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            raise EmailNotValid
        return email


account_active_table = Table(
    "account_active",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("token", String, unique=True, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("expired_at", Float, nullable=False),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("length(token) > 0", name="non_empty_token"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("expired_at >= 0", name="positive_expired_at"),
)

mapper_registry.map_imperatively(AccountActive, account_active_table)
