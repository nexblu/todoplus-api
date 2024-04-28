from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class Avatar:
    query = db_session.query_property()

    def __init__(self, email, token):
        self.email = email
        self.token = token

    def __repr__(self):
        return f"<User {self.email!r}>"


user_avatar = Table(
    "user_avatar",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "username",
        String(collation="C"),
        ForeignKey("user.username", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("avatar", String, nullable=False),
    Column(
        "created_at",
        Float,
        default=lambda: (
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        ).timestamp(),
    ),
    Column(
        "updated_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
)

mapper_registry.map_imperatively(Avatar, user_avatar)
