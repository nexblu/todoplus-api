from .config import db_session, init_db
from models import BookmarkPinDatabase, TodoListDatabase
from .database import Database
from sqlalchemy import and_, desc
from utils import TaskNotFound, BookmarkAlreadyPinned
from .todo_list import TodoListCRUD


class BookmarkPinCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.todo_list_database = TodoListCRUD()

    async def insert(self, user, task_id, bookmark_id, created_at):
        if not (
            task := (
                TodoListDatabase.query.filter(
                    and_(
                        TodoListDatabase.id == task_id,
                        TodoListDatabase.user_id == user.id,
                    )
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            )
        ):
            raise TaskNotFound
        if bookmark_pin := (
            BookmarkPinDatabase.query.filter(
                and_(
                    BookmarkPinDatabase.task_id == task_id,
                    BookmarkPinDatabase.user_id == user.id,
                )
            )
            .order_by(desc(BookmarkPinDatabase.created_at))
            .first()
        ):
            raise BookmarkAlreadyPinned
        new_bookmark_pin = BookmarkPinDatabase(
            user_id=user.id,
            task_id=task_id,
            bookmark_id=bookmark_id,
            created_at=created_at,
        )
        db_session.add(new_bookmark_pin)
        db_session.commit()

        return new_bookmark_pin

    async def delete(self, category, **kwargs):
        pass

    async def get(self, category, **kwargs):
        pass

    async def update(self, category, **kwargs):
        pass
