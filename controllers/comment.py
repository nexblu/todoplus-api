from database import CommentCRUD
from traceback import print_exc
from flask import jsonify
import datetime
from utils import CommentNotFound
from sqlalchemy.exc import IntegrityError


class CommentController:
    def __init__(self) -> None:
        self.comment_database = CommentCRUD()

    async def clear_comment_by_task_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task_id must be greater than 0"}}),
                    400,
                )
        try:
            await self.comment_database.delete(
                "task_id", user_id=user.id, task_id=task_id
            )
        except CommentNotFound:
            return (
                jsonify(
                    {
                        "errors": f"comment user '{user.id}' with task id '{task_id}' not found"
                    }
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success clear comment '{user.id}' with task id '{task_id}'",
                    }
                ),
                201,
            )

    async def get_comment_by_task_id(self, user, task_id):
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task_id must be greater than 0"}}),
                    400,
                )
        try:
            result = await self.comment_database.get(
                "task_id", user_id=user.id, task_id=task_id
            )
        except CommentNotFound:
            return (
                jsonify(
                    {"errors": f"comment user '{user.id}' with '{task_id}' not found"}
                ),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "data": [
                            {
                                "avatar_url": user.avatar_url,
                                "user_id": user.id,
                                "task_id": comment.task_id,
                                "comment_id": comment.id,
                                "comment": comment.comment,
                                "created_at": comment.created_at,
                                "updated_at": comment.updated_at,
                            }
                            for user, comment in result
                        ]
                    }
                ),
                200,
            )

    async def add_comment(self, user, comment, task_id):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        if (not comment or comment.isspace()) and not task_id:
            return (
                jsonify(
                    {
                        "errors": {
                            "task_id": "task id is empety",
                            "comment": "comment is empety",
                        }
                    }
                ),
                400,
            )
        if not comment or comment.isspace():
            return jsonify({"errors": {"comment": "comment is empety"}}), 400
        if not task_id:
            return jsonify({"errors": {"task_id": "task id is empety"}}), 400
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task id must be integer"}}), 400
        else:
            if not task_id > 0:
                return (
                    jsonify({"errors": {"task_id": "task_id must be greater than 0"}}),
                    400,
                )
        try:
            await self.comment_database.insert(
                user.id, comment, task_id, created_at, created_at
            )
        except IntegrityError:
            return (
                jsonify(
                    {
                        "message": f"task '{task_id}' not found",
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "message": f"success add comment task '{task_id}'",
                    }
                ),
                201,
            )
