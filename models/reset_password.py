from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class EmailRequired(Exception):
    def __init__(self, message="email is required"):
        self.message = message
        super().__init__(self.message)


class TokenRequired(Exception):
    def __init__(self, message="token is required"):
        self.message = message
        super().__init__(self.message)


class ResetPassword:
    query = db_session.query_property()

    def __init__(self, email, token):
        if email_space := email.isspace() or not email:
            raise EmailRequired
        else:
            self.email = email
        if token_space := token.isspace() or not token:
            raise TokenRequired
        else:
            self.token = token

    def __repr__(self):
        return f"<User {self.email!r}>"


reset_password_table = Table(
    "reset_password",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "email",
        String(collation="C"),
        ForeignKey("user.email", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("token", String, unique=True, nullable=False),
    Column(
        "created_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column(
        "expired_at",
        Float,
        default=datetime.datetime.now(datetime.timezone.utc).timestamp()
        + (datetime.timedelta(hours=7).total_seconds()),
    ),
)

mapper_registry.map_imperatively(ResetPassword, reset_password_table)
