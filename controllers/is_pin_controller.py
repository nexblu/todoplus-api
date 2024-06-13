from database import TodoListCRUD, IsDoneCRUD, IsPinCRUD, BookmarkCRUD
from utils import TaskNotFound
from flask import jsonify
from sqlalchemy.exc import IntegrityError


class IsPinController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.is_pin_database = IsPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def get_is_pin_by_id(self, user, task_id):
        try:
            result = await self.is_pin_database.get(
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
            author, todo_list, pinned = result
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
                                "is_pin_id": pinned.id,
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

    async def delete_is_pin_by_id(self, user, task_id):
        try:
            await self.is_pin_database.delete(
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
                        "status_code": 201,
                        "message": f"success remove pinned '{task_id}'",
                    }
                ),
                201,
            )

    async def add_is_pin_by_id(self, user, task_id):
        try:
            await self.is_pin_database.insert(user.id, task_id)
        except IntegrityError:
            return (
                jsonify(
                    {
                        "status_code": 400,
                        "message": f"task '{task_id}' already pinned",
                    }
                ),
                400,
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
                        "status_code": 201,
                        "message": f"success pinned task '{task_id}'",
                    }
                ),
                201,
            )

    async def add_is_pin(self, user):
        try:
            await self.is_pin_database.update("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task {user.username!r} not found",
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success pinned all task {user.username!r}",
                    }
                ),
                201,
            )

    async def delete_is_pin(self, user):
        try:
            await self.is_pin_database.delete("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task {user.username!r} not found",
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success clear bookmark {user.username!r}",
                    }
                ),
                201,
            )

    async def get_is_pin(self, user):
        try:
            data = await self.is_pin_database.get("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "status_code": 404,
                        "message": f"task {user.username!r} not found",
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
                                    "is_pin_id": pinned.id,
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
                                for author, todo_list, pinned in data
                            ],
                        },
                    }
                ),
                200,
            )
