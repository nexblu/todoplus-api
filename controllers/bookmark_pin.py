from database import BookmarkPinCRUD
from flask import jsonify
from utils import TaskNotFound, BookmarkAlreadyPinned
import datetime


class BookmarkPinController:
    def __init__(self) -> None:
        self.bookmark_pin = BookmarkPinCRUD()

    async def add_bookmark_pin_by_id(self, user, task_id, bookmark_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        try:
            result = await self.bookmark_pin.insert(
                user, task_id, bookmark_id, created_at
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
