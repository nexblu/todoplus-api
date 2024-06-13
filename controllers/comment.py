from database import CommentCRUD
from traceback import print_exc
from flask import jsonify
import datetime
from utils import CommentNotFound
from sqlalchemy.exc import IntegrityError


class CommentController:
    def __init__(self) -> None:
        self.comment_database = CommentCRUD()

    async def get_comment(self, user):
        try:
            result = await self.comment_database.get("all", user_id=user.id)
        except CommentNotFound:
            return (
                jsonify({"errors": f"comment '{user.id}' not found"}),
                404,
            )
        else:
            return (
                jsonify(
                    {
                        "data": [
                            {
                                "user_id": user.id,
                                "comment_id": comment.id,
                                "comment": comment.comment,
                                "created_at": comment.created_at,
                                "updated_at": comment.updated_at,
                            }
                            for comment in result
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
                            "task_id": "task_id is empety",
                            "comment": "comment is empety",
                        }
                    }
                ),
                400,
            )
        if not comment or comment.isspace():
            return jsonify({"errors": {"comment": "comment is empety"}}), 400
        if not task_id:
            return jsonify({"errors": {"task_id": "task_id is empety"}}), 400
        if not isinstance(task_id, int) and task_id:
            return jsonify({"errors": {"task_id": "task_id must be integer"}}), 400
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
