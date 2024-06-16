from .config import db_session, init_db
from models import BookmarkPinDatabase, TodoListDatabase, UserDatabase, BookmarkDatabase
from .database import Database
from sqlalchemy import and_, desc
from utils import TaskNotFound, BookmarkAlreadyPinned
from .todo_list import TodoListCRUD


class BookmarkPinCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.todo_list_database = TodoListCRUD()

    async def insert(self, user_id, task_id, bookmark_id, created_at):
        if not (
            task := (
                TodoListDatabase.query.filter(
                    and_(
                        TodoListDatabase.id == task_id,
                        TodoListDatabase.user_id == user_id,
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
                    BookmarkPinDatabase.user_id == user_id,
                )
            )
            .order_by(desc(BookmarkPinDatabase.created_at))
            .first()
        ):
            raise BookmarkAlreadyPinned
        new_bookmark_pin = BookmarkPinDatabase(
            user_id=user_id,
            task_id=task_id,
            bookmark_id=bookmark_id,
            created_at=created_at,
        )
        db_session.add(new_bookmark_pin)
        db_session.commit()

        return new_bookmark_pin

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        bookmark_id = kwargs.get("bookmark_id")
        task_id = kwargs.get("task_id")
        if category == "bookmark_id":
            bookmark_pin = BookmarkPinDatabase.query.filter(
                and_(
                    BookmarkPinDatabase.task_id == task_id,
                    BookmarkPinDatabase.user_id == user_id,
                    BookmarkPinDatabase.bookmark_id == bookmark_id,
                )
            ).delete()
            db_session.commit()
            if not bookmark_pin:
                raise TaskNotFound

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        bookmark_id = kwargs.get("bookmark_id")
        task_id = kwargs.get("task_id")
        if category == "bookmark_id":
            if (
                bookmark_pin := db_session.query(
                    UserDatabase,
                    TodoListDatabase,
                    BookmarkDatabase,
                    BookmarkPinDatabase,
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .join(
                    BookmarkPinDatabase,
                    BookmarkDatabase.id == BookmarkPinDatabase.bookmark_id,
                )
                .filter(
                    and_(
                        UserDatabase.id == user_id,
                        TodoListDatabase.id == task_id,
                        BookmarkPinDatabase.bookmark_id == bookmark_id,
                    )
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                return bookmark_pin
            raise TaskNotFound
        elif category == "all":
            if (
                bookmark_pin := db_session.query(
                    UserDatabase,
                    TodoListDatabase,
                    BookmarkDatabase,
                    BookmarkPinDatabase,
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .join(
                    BookmarkPinDatabase,
                    BookmarkDatabase.id == BookmarkPinDatabase.bookmark_id,
                )
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return bookmark_pin
            raise TaskNotFound
        elif category == "is_pin":
            if (
                data := BookmarkPinDatabase.query.filter(
                    and_(
                        BookmarkPinDatabase.task_id == task_id,
                        BookmarkPinDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(BookmarkPinDatabase.created_at))
                .first()
            ):
                return True
            return False
        elif category == "id":
            if (
                data := BookmarkPinDatabase.query.filter(
                    and_(
                        BookmarkPinDatabase.task_id == task_id,
                        BookmarkPinDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(BookmarkPinDatabase.created_at))
                .first()
            ):
                return data.id
            return None

    async def update(self, category, **kwargs):
        pass
