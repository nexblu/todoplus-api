import datetime
from database import TodoListCRUD, IsDoneCRUD, BookmarkCRUD, IsPinCRUD
from flask import jsonify
import datetime
from utils import TaskNotFound, Validator


class TaskController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.is_pin_database = IsPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def add_task(self, user, task, description, tags):
        if errors := await Validator.validate_task(task, tags):
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": errors,
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task": task,
                            "description": description,
                            "tags": tags,
                        },
                    }
                ),
                400,
            )
        result = await self.todo_list_database.insert(
            user.id,
            task,
            description,
            tags,
            datetime.datetime.now(datetime.timezone.utc).timestamp(),
        )
        return (
            jsonify(
                {
                    "success": True,
                    "status_code": 201,
                    "message": f"success add task",
                    "data": {
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "task_id": result.id,
                        "task": result.task,
                        "tags": result.tags,
                        "description": result.description,
                        "date": result.date,
                        "created_at": result.created_at,
                        "updated_at": result.updated_at,
                    },
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
                        "success": False,
                        "status_code": 404,
                        "message": f"task user '{user.username!r}' not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "data": [
                            {
                                "user_id": author.id,
                                "username": author.username,
                                "email": user.email,
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
                ),
                200,
            )

    async def delete_task(self, user):
        try:
            await self.todo_list_database.delete(
                "clear",
                user_id=user.id,
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task user '{user.username!r}' not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                ),
                200,
            )

    async def get_task_by_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {"task_id": "task id must be integer"},
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                400,
            )
        else:
            if not task_id > 0:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status_code": 400,
                            "message": {"task_id": "task id must be greater than 0"},
                            "data": {
                                "user_id": user.id,
                                "username": user.username,
                                "email": user.email,
                                "task_id": task_id,
                            },
                        }
                    ),
                    400,
                )
        try:
            data = await self.todo_list_database.get(
                "task_id", user_id=user.id, task_id=task_id
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task with id '{task_id}' not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                404,
            )
        else:
            author, todo_list = data
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "data": {
                            "user_id": author.id,
                            "username": author.username,
                            "email": user.email,
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
                        },
                    },
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
                        "success": False,
                        "status_code": 404,
                        "message": f"task with id '{task_id}' not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"success delete task with id '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                200,
            )

    async def put_task_by_id(self, user, task_id, new_task):
        try:
            result = await self.todo_list_database.update(
                "new_task", user_id=user.id, task_id=task_id, new_task=new_task
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task with id '{task_id}' not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 201,
                        "message": f"success update task with id '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                            "new_task": result.task,
                            "created_at": result.created_at,
                            "updated_at": result.updated_at,
                        },
                    }
                ),
                201,
            )
