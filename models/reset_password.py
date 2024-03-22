from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class ResetPassword:
    query = db_session.query_property()

    def __init__(self, email, token, created_at):
        self.email = email
        self.token = token
        self.created_at = created_at

    def __repr__(self):
        return f"<User {self.email!r}>"


reset_password = Table(
    "reset_password",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "email",
        String(collation="C"),
        ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("token", String, nullable=False),
    Column("created_at", Float),
)

mapper_registry.map_imperatively(ResetPassword, reset_password)
