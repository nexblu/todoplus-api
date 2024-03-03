from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class User:
    query = db_session.query_property()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="NOCASE")),
    Column("email", String(collation="NOCASE")),
    Column("password", String),
    Column("created_at", Float, default=datetime.datetime.utcnow().timestamp()),
    Column("is_active", Boolean, default=True),
    UniqueConstraint("username", "email", name="uq_user_username_email"),
)

mapper_registry.map_imperatively(User, user)
