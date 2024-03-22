from sqlalchemy import Table, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class User:
    query = db_session.query_property()

    def __init__(self, username, email, password, created_at):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return f"<User {self.username!r}>"


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(collation="C"), unique=True, nullable=False),
    Column("email", String(collation="C"), unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("is_active", Boolean, default=False),
)

mapper_registry.map_imperatively(User, user)
