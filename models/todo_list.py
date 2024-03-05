from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class TodoList:
    query = db_session.query_property()

    def __init__(self, username, task):
        self.username = username
        self.task = task

    def __repr__(self):
        return f"<User {self.username}>"


todo_list = Table(
    "todo_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, ForeignKey("user.username", ondelete="CASCADE")),
    Column("task", String),
    Column("created_at", Float, default=datetime.datetime.utcnow().timestamp()),
    Column("is_done", Boolean, default=False),
    UniqueConstraint("username", name="uq_todo_list_username"),
)

mapper_registry.map_imperatively(TodoList, todo_list)
