from .config import db_session, init_db
from models import TodoList
from .database import Database
from sqlalchemy import func, and_


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

    async def get(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        if type == "username":
            return TodoList.query.filter(
                func.lower(TodoList.username) == username.lower()
            ).all()
        if type == "id":
            return TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()

    async def update(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        new_task = kwargs.get("new_task")
        if type == "id":
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()
            todo.task = new_task
            db_session.commit()
