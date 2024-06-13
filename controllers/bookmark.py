from database import TodoListCRUD, IsDoneCRUD, BookmarkCRUD, IsPinCRUD
from flask import jsonify
from utils import TaskNotFound
from sqlalchemy.exc import IntegrityError


class BookmarkController:
    def __init__(self) -> None:
        self.todo_list_database = TodoListCRUD()
        self.is_done_database = IsDoneCRUD()
        self.is_pin_database = IsPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def get_bookmark_by_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task id must be greater than 0"}}),
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
                        "errors": {
                            "task": f"task {user.username!r} with task '{task_id}' not found"
                        }
                    }
                ),
                404,
            )
        else:
            author, todo_list, bookmark = result
            return (
                jsonify(
                    {
                        "data": {
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
                            "bookmark_id": bookmark.id,
                            "updated_at": todo_list.updated_at,
                            "created_at": todo_list.created_at,
                        }
                    },
                ),
                200,
            )

    async def delete_bookmark_by_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task id must be greater than 0"}}),
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
                        "errors": {
                            "task": f"task {user.username!r} with task '{task_id}' not found"
                        }
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "message": f"success remove bookmark '{task_id}' from user '{user.id}'",
                    }
                ),
                201,
            )

    async def add_bookmark_by_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task id must be greater than 0"}}),
                    400,
                )
        try:
            await self.bookmark_database.insert(user.id, task_id)
        except IntegrityError:
            return (
                jsonify(
                    {
                        "errors": {
                            "user": f"task {user.username!r} with task '{task_id}' already bookmark"
                        }
                    }
                ),
                400,
            )
        except TaskNotFound:
            return (
                jsonify(
                    {
                        "errors": {
                            "task": f"task {user.username!r} with task '{task_id}' not found"
                        }
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "message": f"success add bookmark task '{task_id}'",
                    }
                ),
                201,
            )

    async def add_bookmark(self, user):
        try:
            await self.bookmark_database.update("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify({"errors": {"user": f"task {user.username!r} not found"}}),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "message": f"success bookmark all task {user.username!r}",
                    }
                ),
                201,
            )

    async def delete_bookmark(self, user):
        try:
            await self.bookmark_database.delete("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify({"errors": {"user": f"task {user.username!r} not found"}}),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "message": f"success clear bookmark {user.username!r}",
                    }
                ),
                201,
            )

    async def get_bookmark(self, user):
        try:
            data = await self.bookmark_database.get("all", user_id=user.id)
        except TaskNotFound:
            return (
                jsonify({"errors": {"user": f"task {user.username!r} not found"}}),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "data": [
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
