from database import TodoListCRUD, IsDoneCRUD, BookmarkCRUD, IsPinCRUD
from flask import jsonify
from utils import TaskNotFound, FailedBookmark
from sqlalchemy.exc import IntegrityError


class BookmarkController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.is_pin_database = IsPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def get_bookmark_by_id(self, user, task_id):
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
            result = await self.bookmark_database.get(
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
            author, todo_list, bookmark = result
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"task with id '{task_id}' was found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
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
                            "bookmark_id": bookmark.id,
                            "updated_at": todo_list.updated_at,
                            "created_at": todo_list.created_at,
                        },
                    },
                ),
                200,
            )

    async def delete_bookmark_by_id(self, user, task_id):
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
            await self.bookmark_database.delete(
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
                        "status_code": 201,
                        "message": f"success remove bookmark id '{task_id}' from user {user.username!r}",
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

    async def add_bookmark_by_id(self, user, task_id):
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
            result = await self.bookmark_database.insert(user.id, task_id)
        except IntegrityError:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"task id '{task_id}' already bookmark",
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
                        "message": f"success add bookmark task id '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": result.task_id,
                            "bookmark_id": result.id,
                            "created_at": result.created_at,
                        },
                    }
                ),
                201,
            )

    async def add_bookmark(self, user):
        try:
            result = await self.bookmark_database.update("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task with user {user.username!r} not found",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                404,
            )
        except FailedBookmark:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"failed bookmark all with user id {user.username!r}",
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
                        "message": f"success bookmark all user {user.username!r}",
                        "data": [
                            {
                                "user_id": user.id,
                                "username": user.username,
                                "email": user.email,
                                "task_id": data.task_id,
                                "bookmark_id": data.id,
                                "created_at": data.created_at,
                            }
                            for data in result
                        ],
                    }
                ),
                201,
            )

    async def delete_bookmark(self, user):
        try:
            await self.bookmark_database.delete("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task with user {user.username!r} not found",
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
                        "message": f"success clear bookmark user {user.username!r}",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    }
                ),
                201,
            )

    async def get_bookmark(self, user):
        try:
            data = await self.bookmark_database.get("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 404,
                        "message": f"task with user {user.username!r} not found",
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
                        "message": f"task user {user.username!r} was found",
                        "data": [
                            {
                                "user_id": user.id,
                                "username": user.username,
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
                                "bookmark_id": bookmark.id,
                                "updated_at": todo_list.updated_at,
                                "created_at": todo_list.created_at,
                            }
                            for author, todo_list, bookmark in data
                        ],
                    },
                ),
                200,
            )
