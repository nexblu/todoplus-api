from .config import db_session, init_db
from models import TodoList
from .database import Database


class TodolistDatabase:
    def __init__(self) -> None:
        init_db()

    async def insert(self, username, task):
        todo_list = TodoList(username, task)
        db_session.add(todo_list)
        db_session.commit()

    async def delete(self):
        pass

    async def get(self):
        pass

    async def update(self):
        pass
