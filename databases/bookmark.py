from .config import db_session, init_db
from models import BookmarkDatabase, UserDatabase, TodoListDatabase
from .database import Database
import datetime
from sqlalchemy import desc, and_
from utils import TaskNotFound
from .user import UserCRUD
from .todo_list import TodoListCRUD


class BookmarkCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.user_database = UserCRUD()
        self.todo_list_database = TodoListCRUD()

    async def insert(self, user_id, task_id):
        if (
            data := TodoListDatabase.query.filter(
                and_(
                    TodoListDatabase.id == task_id,
                    TodoListDatabase.user_id == user_id,
                )
            )
            .order_by(desc(TodoListDatabase.created_at))
            .first()
        ):
            created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            is_done = BookmarkDatabase(user_id, task_id, created_at, created_at)
            db_session.add(is_done)
            await self.user_database.update(
                "updated_at", updated_at=created_at, user_id=user_id
            )
            await self.todo_list_database.update(
                "updated_at", updated_at=created_at, user_id=user_id
            )
            db_session.commit()
            return
        raise TaskNotFound

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if category == "task_id":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, BookmarkDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .filter(
                    and_(
                        UserDatabase.id == user_id, BookmarkDatabase.task_id == task_id
                    )
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                user, task, bookmark = data
                db_session.delete(bookmark)
                user.updated_at = created_at
                task.updated_at = created_at
                db_session.commit()
                return
            raise TaskNotFound
        elif category == "all":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, BookmarkDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                for user, task, is_done in data:
                    db_session.delete(is_done)
                await self.user_database.update(
                    "updated_at", updated_at=created_at, user_id=user_id
                )
                await self.todo_list_database.update(
                    "updated_at", updated_at=created_at, user_id=user_id
                )
                db_session.commit()
                return
            raise TaskNotFound

    async def get(self, category, **kwargs):
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")
        if category == "bookmark":
            if (
                data := BookmarkDatabase.query.filter(
                    and_(
                        BookmarkDatabase.task_id == task_id,
                        BookmarkDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(BookmarkDatabase.created_at))
                .first()
            ):
                return True
            return False
        elif category == "task_id":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, BookmarkDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .filter(
                    and_(
                        UserDatabase.id == user_id, BookmarkDatabase.task_id == task_id
                    )
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                return data
            raise TaskNotFound
        elif category == "all":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, BookmarkDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(BookmarkDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return data
            raise TaskNotFound

    async def update(self, category, **kwargs):
        pass
