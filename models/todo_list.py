from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    JSON,
    Date,
)
from sqlalchemy.orm import registry
from databases import metadata, db_session
import datetime

mapper_registry = registry()


class UsernameRequired(Exception):
    def __init__(self, message="username is required"):
        self.message = message
        super().__init__(self.message)


class TaskRequired(Exception):
    def __init__(self, message="task is required"):
        self.message = message
        super().__init__(self.message)


class TagsList(Exception):
    def __init__(self, message="tags must be list"):
        self.message = message
        super().__init__(self.message)


class MaxTags5(Exception):
    def __init__(self, message="max tags is 5"):
        self.message = message
        super().__init__(self.message)


class TodoList:
    query = db_session.query_property()

    def __init__(self, username, task, tags, date):
        if username_space := username.isspace() or not username:
            raise UsernameRequired
        else:
            self.username = username
        if task_space := task.isspace() or not task:
            raise TaskRequired
        else:
            self.task = task
        if not isinstance(tags, list):
            raise TagsList
        else:
            if len(tags) > 5:
                raise MaxTags5
            else:
                self.tags = tags
        self.date = date

    def __repr__(self):
        return f"<User {self.username!r}>"


todo_list_table = Table(
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
    Column("tags", JSON, nullable=True),
    Column("date", Date, nullable=True),
    Column(
        "update_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column(
        "created_at",
        Float,
        default=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
    Column("is_pin", Boolean, default=False),
    Column("bookmark", Boolean, default=False),
    Column("is_done", Boolean, default=False),
)

mapper_registry.map_imperatively(TodoList, todo_list_table)
