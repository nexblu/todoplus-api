from .config import db_session, init_db
from models import BookmarkPinDatabase, TodoListDatabase
from .database import Database
from sqlalchemy import and_, desc
from utils import UserNotFound, TaskNotFound, BookmarkAlreadyPinned
import datetime
from .todo_list import TodoListCRUD


class BookmarkPinCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.todo_list_database = TodoListCRUD()

    async def insert(self, user, task_id, bookmark_id, created_at):
        if (
            data := TodoListDatabase.query.filter(
                and_(
                    TodoListDatabase.id == task_id,
                    TodoListDatabase.user_id == user.id,
                )
            )
            .order_by(desc(TodoListDatabase.created_at))
            .first()
        ):
            if not (
                data := BookmarkPinDatabase.query.filter(
                    and_(
                        BookmarkPinDatabase.task_id == task_id,
                        BookmarkPinDatabase.user_id == user.id,
                    )
                )
                .order_by(desc(BookmarkPinDatabase.created_at))
                .first()
            ):
                bookmark_pin = BookmarkPinDatabase(
                    user.id, task_id, bookmark_id, created_at
                )
                db_session.add(bookmark_pin)
                db_session.commit()
                return bookmark_pin
            raise BookmarkAlreadyPinned
        raise TaskNotFound

    async def delete(self, category, **kwargs):
        pass

    async def get(self, category, **kwargs):
        pass

    async def update(self, category, **kwargs):
        pass
