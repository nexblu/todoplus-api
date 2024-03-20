from sqlalchemy import Table, Column, Integer, String, Boolean, Float
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
        return f"<User {self.username!r}>"


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="C"), unique=True, nullable=False),
    Column("email", String(collation="C"), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column(
        "created_at",
        Float,
        default=datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column("is_active", Boolean, default=False),
)

mapper_registry.map_imperatively(User, user)
