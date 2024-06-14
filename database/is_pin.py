from .config import db_session, init_db
from models import TaskPinDatabase, UserDatabase, TodoListDatabase
from .database import Database
import datetime
from sqlalchemy import desc, and_
from utils import TaskNotFound, FailedPinned
from .user import UserCRUD
from .todo_list import TodoListCRUD


class IsPinCRUD(Database):
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
            is_pin = TaskPinDatabase(user_id, task_id, created_at)
            db_session.add(is_pin)
            await self.user_database.update(
                "updated_at", updated_at=created_at, user_id=user_id
            )
            await self.todo_list_database.update(
                "updated_at_task_id",
                updated_at=created_at,
                user_id=user_id,
                task_id=task_id,
            )
            db_session.commit()
            return is_pin
        raise TaskNotFound

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if category == "all":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, TaskPinDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(TaskPinDatabase)
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
        elif category == "task_id":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, TaskPinDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(TaskPinDatabase)
                .filter(
                    and_(UserDatabase.id == user_id, TaskPinDatabase.task_id == task_id)
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                user, task, is_done = data
                db_session.delete(is_done)
                user.updated_at = created_at
                task.updated_at = created_at
                db_session.commit()
                return
            raise TaskNotFound

    async def get(self, category, **kwargs):
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")
        if category == "is_pin":
            if (
                data := TaskPinDatabase.query.filter(
                    and_(
                        TaskPinDatabase.task_id == task_id,
                        TaskPinDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(TaskPinDatabase.created_at))
                .first()
            ):
                return True
            return False
        elif category == "is_pin_id":
            if (
                data := TaskPinDatabase.query.filter(
                    and_(
                        TaskPinDatabase.task_id == task_id,
                        TaskPinDatabase.user_id == user_id,
                    )
                )
                .order_by(desc(TaskPinDatabase.created_at))
                .first()
            ):
                return data.id
            return None
        elif category == "all":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, TaskPinDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(TaskPinDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return data
            raise TaskNotFound
        elif category == "task_id":
            if (
                data := db_session.query(
                    UserDatabase, TodoListDatabase, TaskPinDatabase
                )
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .join(TaskPinDatabase)
                .filter(
                    and_(UserDatabase.id == user_id, TaskPinDatabase.task_id == task_id)
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                return data
            raise TaskNotFound

    async def update(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if category == "all":
            if (
                todo := TodoListDatabase.query.filter(
                    TodoListDatabase.user_id == user_id
                )
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                arr = []
                for data in todo:
                    if not (
                        is_pin_ := await self.get(
                            "is_pin_id", user_id=user_id, task_id=data.id
                        )
                    ):
                        is_pin = TaskPinDatabase(user_id, data.id, created_at)
                        db_session.add(is_pin)
                        arr.append(is_pin)
                if arr:
                    db_session.commit()
                    await self.user_database.update(
                        "updated_at", updated_at=created_at, user_id=user_id
                    )
                    await self.todo_list_database.update(
                        "updated_at", updated_at=created_at, user_id=user_id
                    )
                    return arr
                raise FailedPinned
            raise TaskNotFound
