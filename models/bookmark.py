from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session

mapper_registry = registry()


class BookmarkDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, task_id, created_at, updated_at):
        self.user_id = user_id
        self.task_id = task_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Bookmark '{self.user_id}'>"


bookmark_table = Table(
    "bookmark",
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
        nullable=False,
    ),
    Column("created_at", Float, nullable=False),
    Column("updated_at", Float, nullable=False),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("task_id >= 0", name="positive_task_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
    CheckConstraint("updated_at >= 0", name="positive_updated_at"),
)

mapper_registry.map_imperatively(BookmarkDatabase, bookmark_table)