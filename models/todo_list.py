from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from database import metadata, db_session
from sqlalchemy.dialects.postgresql import JSONB

mapper_registry = registry()


class TodoListDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, task, description, tags, date, created_at, updated_at):
        self.user_id = user_id
        self.task = task
        self.description = description
        self.tags = tags
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<TodoList '{self.user_id}'>"


todo_list_table = Table(
    "todo_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("task", String, nullable=False),
    Column("description", String, nullable=True),
    Column("date", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    Column("created_at", Float, nullable=False),
    Column("tags", JSONB, default=[]),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("length(task) > 0", name="non_empty_task"),
    CheckConstraint(
        "(length(task) > 0) OR (task IS NULL)", name="validate_description_task"
    ),
    CheckConstraint("date > 0", name="positive_date"),
    CheckConstraint(
        "jsonb_array_length(tags) BETWEEN 1 AND 5", name="tags_length_between_1_and_5"
    ),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
)

mapper_registry.map_imperatively(TodoListDatabase, todo_list_table)
