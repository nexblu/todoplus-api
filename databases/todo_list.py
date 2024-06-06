from .config import db_session, init_db
from models import TodoListDatabase
from .database import Database
from sqlalchemy import func, and_
import datetime


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

    async def insert(self, username, task, tags, date):
        todo_list = TodoListDatabase(username, task, tags, date)
        db_session.add(todo_list)
        db_session.commit()
        return todo_list

    async def delete(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        tags = kwargs.get("tags")
        if type == "task":
            todo = TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first()
            if todo:
                db_session.delete(todo)
                db_session.commit()
            else:
                raise TaskNotFoundError(f"task {id} not found")
        elif type == "username":
            todos = (
                TodoListDatabase.query.filter(
                    func.lower(TodoListDatabase.username) == username.lower()
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )
            if todos:
                for todo in todos:
                    db_session.delete(todo)
                db_session.commit()
            else:
                raise TaskNotFoundError(f"user {username!r} not found")
        elif type == "tags":
            todo = TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first()
            if not todo:
                raise TaskNotFoundError(f"task {id} not found")
            else:
                data_tags = todo.tags[:]
                for tag in tags:
                    if tag in data_tags:
                        data_tags.remove(tag)
                    else:
                        raise InvalidTags(f"Tag {tag} not found")
                todo.tags = data_tags
                db_session.commit()

    async def get(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        if type == "username":
            return (
                TodoListDatabase.query.filter(
                    func.lower(TodoListDatabase.username) == username.lower()
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )
        elif type == "id":
            return TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first()
        elif type == "completed":
            return (
                TodoListDatabase.query.filter(
                    and_(
                        func.lower(TodoListDatabase.username) == username.lower(),
                        TodoListDatabase.is_done == True,
                    )
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )
        elif type == "inclomplete":
            return (
                TodoListDatabase.query.filter(
                    and_(
                        func.lower(TodoListDatabase.username) == username.lower(),
                        TodoListDatabase.is_done == False,
                    )
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )
        elif type == "bookmark":
            return (
                TodoListDatabase.query.filter(
                    and_(
                        func.lower(TodoListDatabase.username) == username.lower(),
                        TodoListDatabase.bookmark == True,
                    )
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )
        elif type == "pinned":
            return (
                TodoListDatabase.query.filter(
                    and_(
                        func.lower(TodoListDatabase.username) == username.lower(),
                        TodoListDatabase.is_pin == True,
                    )
                )
                .order_by(TodoListDatabase.created_at)
                .all()
            )

    async def update(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        new_task = kwargs.get("new_task")
        if type == "is_done":
            if todo := TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first():
                todo.is_done = not todo.is_done
                todo.update_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise TaskNotFoundError(f"task {id} not found")
        elif type == "bookmark":
            if todo := TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first():
                todo.bookmark = not todo.bookmark
                todo.update_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
                return todo
            else:
                raise TaskNotFoundError(f"task {id} not found")
        elif type == "task":
            if todo := TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).first():
                todo.task = new_task
                todo.update_at = datetime.datetime.now(
                    datetime.timezone.utc
                ).timestamp()
                db_session.commit()
            else:
                raise TaskNotFoundError(f"task {id} not found")
        elif type == "pinned":
            todo = TodoListDatabase.query.filter(
                and_(
                    func.lower(TodoListDatabase.username) == username.lower(),
                    TodoListDatabase.id == id,
                )
            ).all()
            if todo:
                todo_is_pin = TodoListDatabase.query.filter(
                    and_(
                        func.lower(TodoListDatabase.username) == username.lower(),
                        TodoListDatabase.id == id,
                        TodoListDatabase.is_pin == True,
                    )
                ).all()
                if todo_is_pin:
                    if len(todo_is_pin) < 3:
                        for i in todo:
                            if i.id == id:
                                i.is_pin = not i.is_pin
                                i.update_at = datetime.datetime.now(
                                    datetime.timezone.utc
                                ).timestamp()
                                db_session.commit()
                    else:
                        raise MaxPinned3
                else:
                    pinned_tasks_count = TodoListDatabase.query.filter(
                        and_(
                            func.lower(TodoListDatabase.username) == username.lower(),
                            TodoListDatabase.is_pin == True,
                        )
                    ).count()

                    if pinned_tasks_count < 3:
                        for i in todo:
                            if i.id == id:
                                i.is_pin = not i.is_pin
                                i.update_at = datetime.datetime.now(
                                    datetime.timezone.utc
                                ).timestamp()
                                db_session.commit()
                    else:
                        raise MaxPinned3
            else:
                raise TaskNotFoundError(f"task {id} not found")
