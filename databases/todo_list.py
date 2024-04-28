from .config import db_session, init_db
from models import TodoList
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


class TodolistDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        init_db()

    async def insert(self, username, task, tags, date):
        todo_list = TodoList(username, task, tags, date)
        db_session.add(todo_list)
        db_session.commit()
        return todo_list

    async def delete(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        tags = kwargs.get("tags")
        if type == "task":
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).first()
            if todo:
                db_session.delete(todo)
                db_session.commit()
            else:
                raise TaskNotFoundError(f"task {id} not found")
        elif type == "username":
            todos = (
                TodoList.query.filter(func.lower(TodoList.username) == username.lower())
                .order_by(TodoList.created_at)
                .all()
            )
            if todos:
                for todo in todos:
                    db_session.delete(todo)
                db_session.commit()
            else:
                raise TaskNotFoundError(f"user {username!r} not found")
        elif type == "tags":
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
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
        elif type == "bookmark":
            return (
                TodoList.query.filter(
                    and_(
                        func.lower(TodoList.username) == username.lower(),
                        TodoList.bookmark == True,
                    )
                )
                .order_by(TodoList.created_at)
                .all()
            )
        elif type == "pinned":
            return (
                TodoList.query.filter(
                    and_(
                        func.lower(TodoList.username) == username.lower(),
                        TodoList.is_pin == True,
                    )
                )
                .order_by(TodoList.created_at)
                .all()
            )

    async def update(self, type, **kwargs):
        username = kwargs.get("username")
        id = kwargs.get("id")
        new_task = kwargs.get("new_task")
        if type == "is_done":
            if todo := TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
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
            if todo := TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
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
            if todo := TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
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
            todo = TodoList.query.filter(
                and_(
                    func.lower(TodoList.username) == username.lower(),
                    TodoList.id == id,
                )
            ).all()
            if todo:
                todo_is_pin = TodoList.query.filter(
                    and_(
                        func.lower(TodoList.username) == username.lower(),
                        TodoList.id == id,
                        TodoList.is_pin == True,
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
                    pinned_tasks_count = TodoList.query.filter(
                        and_(
                            func.lower(TodoList.username) == username.lower(),
                            TodoList.is_pin == True,
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
