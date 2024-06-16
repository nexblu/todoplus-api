from database import (
    TodoListCRUD,
    IsDoneCRUD,
    TaskPinCRUD,
    BookmarkCRUD,
    BookmarkPinCRUD,
)
from utils import TaskNotFound, FailedPinned, TaskAlreadyPinned
from flask import jsonify


class TaskPinController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.task_pin_database = TaskPinCRUD()
        self.bookmark_database = BookmarkCRUD()
        self.bookmark_pin_database = BookmarkPinCRUD()

    async def get_is_pin_by_id(self, user, task_id):
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
            result = await self.task_pin_database.get(
                "task_id", user_id=user.id, task_id=task_id
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task id '{task_id}' not found",
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
            author, todo_list, pinned = result
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"data {user.username!r} was found",
                        "result": {
                            "task": {
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
                                "task_pin": await self.task_pin_database.get(
                                    "task_pin", task_id=todo_list.id, user_id=author.id
                                ),
                                "task_pin_id": pinned.id,
                                "bookmark": await self.bookmark_database.get(
                                    "bookmark", task_id=todo_list.id, user_id=author.id
                                ),
                                "bookmark_id": await self.bookmark_database.get(
                                    "bookmark_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "bookmark_pin": await self.bookmark_pin_database.get(
                                    "is_pin", user_id=user.id, task_id=todo_list.task_id
                                ),
                                "bookmark_pin_id": await self.bookmark_pin_database.get(
                                    "id", user_id=user.id, task_id=todo_list.task_id
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
            await self.task_pin_database.delete(
                "task_id", user_id=user.id, task_id=task_id
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task id '{task_id}' not found",
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
                        "message": f"success remove pinned '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                        },
                    }
                ),
                201,
            )

    async def add_is_pin_by_id(self, user, task_id):
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
            result = await self.task_pin_database.insert(user.id, task_id)
        except TaskAlreadyPinned:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"task id '{task_id}' already pinned",
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
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"task id '{task_id}' not found",
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
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 201,
                        "message": f"success pinned task id '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                            "task_pin_id": result.id,
                            "created_at": result.created_at,
                        },
                    }
                ),
                201,
            )

    async def add_is_pin(self, user):
        try:
            result = await self.task_pin_database.update("all", user_id=user.id)
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
        except FailedPinned:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"failed pinned all task user '{user.username!r}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 201,
                        "message": f"success pinned all task user {user.username!r}",
                        "data": [
                            {
                                "user_id": user.id,
                                "username": user.username,
                                "email": user.email,
                                "task_id": data.task_id,
                                "task_pin_id": data.id,
                                "created_at": data.created_at,
                            }
                            for data in result
                        ],
                    }
                ),
                201,
            )

    async def delete_is_pin(self, user):
        try:
            await self.task_pin_database.delete("all", user_id=user.id)
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
                        "status_code": 201,
                        "message": f"success clear task pinned '{user.username!r}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                201,
            )

    async def get_is_pin(self, user):
        try:
            data = await self.task_pin_database.get("all", user_id=user.id)
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
                                "task_pin": await self.task_pin_database.get(
                                    "task_pin",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "task_pin_id": pinned.id,
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
                                "bookmark_pin": await self.bookmark_pin_database.get(
                                    "is_pin", user_id=user.id, task_id=todo_list.task_id
                                ),
                                "bookmark_pin_id": await self.bookmark_pin_database.get(
                                    "id", user_id=user.id, task_id=todo_list.task_id
                                ),
                                "updated_at": todo_list.updated_at,
                                "created_at": todo_list.created_at,
                            }
                            for author, todo_list, pinned in data
                        ],
                    },
                ),
                200,
            )
