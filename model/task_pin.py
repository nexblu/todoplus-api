from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from repository import metadata, db_session

mapper_registry = registry()


class TaskPinDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, task_id, created_at):
        self.user_id = user_id
        self.task_id = task_id
        self.created_at = created_at

    def __repr__(self):
        return f"<TaskPin '{self.user_id}'>"


task_pin_table = Table(
    "task_pin",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "task_id",
        Integer,
        ForeignKey("todo_list.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("created_at", Float, nullable=False),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("task_id >= 0", name="positive_task_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
)

mapper_registry.map_imperatively(TaskPinDatabase, task_pin_table)
