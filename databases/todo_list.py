from .config import db_session, init_db
from models import TodoListDatabase, UserDatabase
from .database import Database
from sqlalchemy import func, and_, desc
import datetime
from .user import UserCRUD
from utils import TaskNotFound


class TaskNotFoundError(Exception):
    def __init__(self, message="task not found"):
        self.message = message
        super().__init__(self.message)


class InvalidTags(Exception):
    def __init__(self, message="invalid tags"):
        self.message = message
        super().__init__(self.message)


class MaxPinned3(Exception):
    def __init__(self, message="max pinned task is 3"):
        self.message = message
        super().__init__(self.message)


class TodolistCRUD(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()
        self.user_database = UserCRUD()

    async def insert(self, user_id, email, task, tags, date):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        todo_list = TodoListDatabase(user_id, task, tags, date, created_at, created_at)
        db_session.add(todo_list)
        db_session.commit()
        await self.user_database.update(
            "updated_at", updated_at=created_at, email=email
        )
        return todo_list

    async def delete(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        email = kwargs.get("email")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if category == "clear":
            if (
                data := TodoListDatabase.query.filter(
                    TodoListDatabase.user_id == user_id
                )
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                for d in data:
                    db_session.delete(d)
                db_session.commit()
                await self.user_database.update(
                    "updated_at", updated_at=created_at, email=email
                )
                return
            raise TaskNotFound

    async def get(self, category, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        if category == "is-done":
            if (
                data := db_session.query(UserDatabase, TodoListDatabase)
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return data
            raise TaskNotFound
        elif category == "all":
            if (
                data := db_session.query(UserDatabase, TodoListDatabase)
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .filter(UserDatabase.id == user_id)
                .order_by(desc(TodoListDatabase.created_at))
                .all()
            ):
                return data
            raise TaskNotFound
        elif category == "task_id":
            if (
                data := db_session.query(UserDatabase, TodoListDatabase)
                .select_from(UserDatabase)
                .join(TodoListDatabase)
                .filter(
                    and_(UserDatabase.id == user_id, TodoListDatabase.id == task_id)
                )
                .order_by(desc(TodoListDatabase.created_at))
                .first()
            ):
                return data
            raise TaskNotFound

    async def update(self, type, **kwargs):
        user_id = kwargs.get("user_id")
        is_done = kwargs.get("is_done")
        email = kwargs.get("email")
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if type == "is-done":
            if todo := TodoListDatabase.query.filter(
                TodoListDatabase.user_id == user_id
            ).all():
                for data in todo:
                    data.is_done = is_done
                    data.updated_at = created_at
                db_session.commit()
                await self.user_database.update(
                    "updated_at", updated_at=created_at, email=email
                )
                return
            raise TaskNotFound
        # elif type == "bookmark":
        #     if todo := TodoListDatabase.query.filter(
        #         and_(
        #             func.lower(TodoListDatabase.username) == username.lower(),
        #             TodoListDatabase.id == id,
        #         )
        #     ).first():
        #         todo.bookmark = not todo.bookmark
        #         todo.update_at = datetime.datetime.now(
        #             datetime.timezone.utc
        #         ).timestamp()
        #         db_session.commit()
        #         return todo
        #     else:
        #         raise TaskNotFoundError(f"task {id} not found")
        # elif type == "task":
        #     if todo := TodoListDatabase.query.filter(
        #         and_(
        #             func.lower(TodoListDatabase.username) == username.lower(),
        #             TodoListDatabase.id == id,
        #         )
        #     ).first():
        #         todo.task = new_task
        #         todo.update_at = datetime.datetime.now(
        #             datetime.timezone.utc
        #         ).timestamp()
        #         db_session.commit()
        #     else:
        #         raise TaskNotFoundError(f"task {id} not found")
        # elif type == "pinned":
        #     todo = TodoListDatabase.query.filter(
        #         and_(
        #             func.lower(TodoListDatabase.username) == username.lower(),
        #             TodoListDatabase.id == id,
        #         )
        #     ).all()
        #     if todo:
        #         todo_is_pin = TodoListDatabase.query.filter(
        #             and_(
        #                 func.lower(TodoListDatabase.username) == username.lower(),
        #                 TodoListDatabase.id == id,
        #                 TodoListDatabase.is_pin == True,
        #             )
        #         ).all()
        #         if todo_is_pin:
        #             if len(todo_is_pin) < 3:
        #                 for i in todo:
        #                     if i.id == id:
        #                         i.is_pin = not i.is_pin
        #                         i.update_at = datetime.datetime.now(
        #                             datetime.timezone.utc
        #                         ).timestamp()
        #                         db_session.commit()
        #             else:
        #                 raise MaxPinned3
        #         else:
        #             pinned_tasks_count = TodoListDatabase.query.filter(
        #                 and_(
        #                     func.lower(TodoListDatabase.username) == username.lower(),
        #                     TodoListDatabase.is_pin == True,
        #                 )
        #             ).count()

        #             if pinned_tasks_count < 3:
        #                 for i in todo:
        #                     if i.id == id:
        #                         i.is_pin = not i.is_pin
        #                         i.update_at = datetime.datetime.now(
        #                             datetime.timezone.utc
        #                         ).timestamp()
        #                         db_session.commit()
        #             else:
        #                 raise MaxPinned3
        #     else:
        #         raise TaskNotFoundError(f"task {id} not found")
