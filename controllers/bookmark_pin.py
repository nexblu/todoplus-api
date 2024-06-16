from database import BookmarkPinCRUD, IsDoneCRUD, TaskPinCRUD, BookmarkCRUD
from flask import jsonify
from utils import TaskNotFound, BookmarkAlreadyPinned
import datetime


class BookmarkPinController:
    def __init__(self) -> None:
        self.bookmark_pin = BookmarkPinCRUD()
        self.is_done_database = IsDoneCRUD()
        self.task_pin_database = TaskPinCRUD()
        self.bookmark_database = BookmarkCRUD()

    async def get_bookmark_pin_by_id(self, user, task_id, bookmark_id):
        try:
            result = await self.bookmark_pin.get(
                "bookmark_id", user_id=user.id, bookmark_id=bookmark_id, task_id=task_id
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
                            "bookmark_id": bookmark_id,
                        },
                    }
                ),
                404,
            )
        else:
            author, todo_list, bookmark, bookmark_pin = result
            return (
                jsonify(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": f"bookmark id '{bookmark_id}' was found",
                        "data": {
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
                            "task_pin_id": await self.task_pin_database.get(
                                "task_pin_id",
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
                            "bookmark_pin": True,
                            "bookmark_pin_id": bookmark_pin.id,
                            "updated_at": todo_list.updated_at,
                            "created_at": todo_list.created_at,
                        },
                    }
                ),
                200,
            )

    async def delete_bookmark_pin_by_id(self, user, task_id, bookmark_id):
        try:
            await self.bookmark_pin.delete(
                "bookmark_id", user_id=user.id, bookmark_id=bookmark_id, task_id=task_id
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
                            "bookmark_id": bookmark_id,
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
                        "message": f"success remove pin bookmark id '{bookmark_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                            "bookmark_id": bookmark_id,
                        },
                    }
                ),
                201,
            )

    async def add_bookmark_pin_by_id(self, user, task_id, bookmark_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        try:
            result = await self.bookmark_pin.insert(
                user.id, task_id, bookmark_id, created_at
            )
        except BookmarkAlreadyPinned:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": f"bookmark id '{bookmark_id}' already pinned",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": task_id,
                            "bookmark_id": bookmark_id,
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
                        "message": f"success pin bookmark id '{bookmark_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": result.task_id,
                            "bookmark_id": result.bookmark_id,
                            "pin_bookmark_id": result.id,
                            "created_at": result.created_at,
                        },
                    }
                ),
                201,
            )
