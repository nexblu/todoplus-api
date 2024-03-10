from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class TodoList:
    query = db_session.query_property()

    def __init__(self, username, task, created_at, is_done):
        self.username = username
        self.task = task
        self.created_at = created_at
        self.is_done = is_done

    def __repr__(self):
        return f"<User {self.username!r}>"


todo_list = Table(
    "todo_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "username",
        String(collation="C"),
        ForeignKey("user.username", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("task", String, nullable=False),
    Column("created_at", Float, default=datetime.datetime.utcnow().timestamp()),
    Column("is_done", Boolean, default=False),
)

mapper_registry.map_imperatively(TodoList, todo_list)
