import datetime
from database import TodoListCRUD, IsDoneCRUD, BookmarkCRUD, IsPinCRUD
from flask import jsonify
import datetime
from sqlalchemy.exc import IntegrityError, DataError
from utils import TaskNotFound
import traceback


class TaskController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.is_pin_database = IsPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def add_task(self, user, task,description, tags):
        try:
            await self.todo_list_database.insert(
                user.id,
                task,
                description,
                tags,
                datetime.datetime.now(datetime.timezone.utc).timestamp(),
            )
        except (IntegrityError, DataError):
            traceback.print_exc()
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"data is invalid",
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success create task {task!r}",
                    }
                ),
                201,
            )

    async def get_task(self, user):
        try:
            data = await self.todo_list_database.get(
                "all",
                user_id=user.id,
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task {user.username!r} not found",
                        "result": None,
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "result": {
                            "task": [
                                {
                                    "user_id": author.id,
                                    "username": author.username,
                                    "task_id": todo_list.id,
                                    "task": todo_list.task,
                                    "date": todo_list.date,
                                    "tags": todo_list.tags,
                                    "is_done": await self.is_done_database.get(
                                        "is_done",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_done_id": await self.is_done_database.get(
                                        "is_done_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_pin": await self.is_pin_database.get(
                                        "is_pin",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_pin_id": await self.is_pin_database.get(
                                        "is_pin_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "bookmark": await self.bookmark_database.get(
                                        "bookmark",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "bookmark_id": await self.bookmark_database.get(
                                        "bookmark_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "updated_at": todo_list.updated_at,
                                    "created_at": todo_list.created_at,
                                }
                                for author, todo_list in data
                            ],
                        },
                    }
                ),
                200,
            )

    async def delete_task(self, user):
        try:
            data = await self.todo_list_database.get(
                "all",
                user_id=user.id,
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task {user.username!r} not found",
                        "result": None,
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "result": {
                            "task": [
                                {
                                    "user_id": author.id,
                                    "username": author.username,
                                    "task_id": todo_list.id,
                                    "task": todo_list.task,
                                    "date": todo_list.date,
                                    "tags": todo_list.tags,
                                    "is_done": await self.is_done_database.get(
                                        "is_done",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_done_id": await self.is_done_database.get(
                                        "is_done_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_pin": await self.is_pin_database.get(
                                        "is_pin",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "is_pin_id": await self.is_pin_database.get(
                                        "is_pin_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "bookmark": await self.bookmark_database.get(
                                        "bookmark",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "bookmark_id": await self.bookmark_database.get(
                                        "bookmark_id",
                                        task_id=todo_list.id,
                                        user_id=author.id,
                                    ),
                                    "updated_at": todo_list.updated_at,
                                    "created_at": todo_list.created_at,
                                }
                                for author, todo_list in data
                            ],
                        },
                    }
                ),
                200,
            )

    async def get_task_by_id(self, user, task_id):
        try:
            data = await self.todo_list_database.get(
                "task_id", user_id=user.id, task_id=task_id
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task '{task_id}' not found",
                        "result": None,
                    }
                ),
                404,
            )
        else:
            author, todo_list = data
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "result": {
                            "task": {
                                "user_id": author.id,
                                "username": author.username,
                                "task_id": todo_list.id,
                                "task": todo_list.task,
                                "date": todo_list.date,
                                "tags": todo_list.tags,
                                "is_done": await self.is_done_database.get(
                                    "is_done", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_done_id": await self.is_done_database.get(
                                    "is_done_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "is_pin": await self.is_pin_database.get(
                                    "is_pin", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_pin_id": await self.is_pin_database.get(
                                    "is_pin_id", task_id=todo_list.id, user_id=author.id
                                ),
                                "bookmark": await self.bookmark_database.get(
                                    "bookmark", task_id=todo_list.id, user_id=author.id
                                ),
                                "bookmark_id": await self.bookmark_database.get(
                                    "bookmark_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "updated_at": todo_list.updated_at,
                                "created_at": todo_list.created_at,
                            }
                        },
                    }
                ),
                200,
            )

    async def delete_task_by_id(self, user, task_id):
        try:
            await self.todo_list_database.delete(
                "task_id", user_id=user.id, task_id=task_id
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task '{task_id}' not found",
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "message": f"success delete task {user.username!r} with id '{task_id}'",
                    }
                ),
                200,
            )

    async def put_task_by_id(self, user, task_id, new_task):
        try:
            await self.todo_list_database.update(
                "new_task", user_id=user.id, task_id=task_id, new_task=new_task
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task '{task_id}' not found",
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 200,
                        "message": f"success update task {user.username!r} with id '{task_id}'",
                    }
                ),
                200,
            )
