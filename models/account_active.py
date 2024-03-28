from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class AccountActive:
    query = db_session.query_property()

    def __init__(self, email, token):
        self.email = email
        self.token = token

    def __repr__(self):
        return f"<User {self.email!r}>"


acoount_active = Table(
    "acoount_active",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "email",
        String(collation="C"),
        ForeignKey("user.email", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("token", String, nullable=False),
    Column(
        "expired_at",
        Float,
        default=lambda: (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)).timestamp(),
    ),
    Column(
        "created_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
)

mapper_registry.map_imperatively(AccountActive, acoount_active)
