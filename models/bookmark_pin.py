from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import registry
from database import metadata, db_session

mapper_registry = registry()


class BookmarkPinDatabase:
    query = db_session.query_property()

    def __init__(self, user_id, task_id, created_at):
        self.user_id = user_id
        self.task_id = task_id
        self.created_at = created_at

    def __repr__(self):
        return f"<BookmarkPin '{self.user_id}'>"


bookmark_pin_table = Table(
    "bookmark_pin",
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
        ForeignKey("bookmark.task_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column(
        "bookmark_id",
        Integer,
        ForeignKey("bookmark.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    ),
    Column("created_at", Float, nullable=False),
    CheckConstraint("user_id >= 0", name="positive_user_id"),
    CheckConstraint("task_id >= 0", name="positive_task_id"),
    CheckConstraint("created_at >= 0", name="positive_created_at"),
)

mapper_registry.map_imperatively(BookmarkPinDatabase, bookmark_pin_table)
