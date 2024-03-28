from .config import db_session, init_db
from models import TodoList
from .database import Database
from sqlalchemy import func, and_
import datetime


class TodolistDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, username, task):
        todo_list = TodoList(username, task)
        db_session.add(todo_list)
        db_session.commit()

    async def delete(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        todo = TodoList.query.filter(
            and_(
                func.lower(TodoList.username) == username.lower(),
                TodoList.id == id,
            )
        ).first()
        if type == "task":
            db_session.delete(todo)
            db_session.commit()

    async def get(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        if type == "username":
            return (
                TodoList.query.filter(func.lower(TodoList.username) == username.lower())
                .order_by(TodoList.created_at)
                .all()
            )
        elif type == "id":
            return TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()
        elif type == "completed":
            return (
                TodoList.query.filter(
                    and_(
                        func.lower(TodoList.username) == username.lower(),
                        TodoList.is_done == True,
                    )
                )
                .order_by(TodoList.created_at)
                .all()
            )
        elif type == "inclomplete":
            return (
                TodoList.query.filter(
                    and_(
                        func.lower(TodoList.username) == username.lower(),
                        TodoList.is_done == False,
                    )
                )
                .order_by(TodoList.created_at)
                .all()
            )

    async def update(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        new_task = kwargs.get("new_task")
        is_done = kwargs.get("is_done")
        if type == "is_done":
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()
            todo.is_done = is_done
            todo.update_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            db_session.commit()
        elif type == "task":
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()
            todo.task = new_task
            todo.update_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
            db_session.commit()
