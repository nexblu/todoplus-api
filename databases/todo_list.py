from .config import db_session, init_db
from models import TodoList


def add_todo_list(username, task):
    init_db()
    todo_list = TodoList(username, task)
    db_session.add(todo_list)
    db_session.commit()
