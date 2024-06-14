from database import CommentCRUD
from flask import jsonify
import datetime
from utils import CommentNotFound
from sqlalchemy.exc import IntegrityError


class CommentController:
    def __init__(self) -> None:
        self.comment_database = CommentCRUD()

    async def clear_comment_by_task_id(self, user, task_id):
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
            await self.comment_database.delete(
                "task_id", user_id=user.id, task_id=task_id
            )
        except CommentNotFound:
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
                        "message": f"success clear comment task id '{task_id}'",
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

    async def get_comment_by_task_id(self, user, task_id):
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
            result = await self.comment_database.get(
                "task_id", user_id=user.id, task_id=task_id
            )
        except CommentNotFound:
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
                        "message": f"comment task id '{task_id}' was found",
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
                        ],
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
                        "success": False,
                        "status_code": 400,
                        "message": {
                            "task_id": "task id is empety",
                            "comment": "comment is empety",
                        },
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
        if not comment or comment.isspace():
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {
                            "comment": "comment is empety",
                        },
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
        if not task_id:
            return (
                jsonify(
                    {
                        "success": False,
                        "status_code": 400,
                        "message": {"task_id": "task id is empety"},
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
            result = await self.comment_database.insert(
                user.id, comment, task_id, created_at, created_at
            )
        except IntegrityError:
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
                        "message": f"success add comment task id '{task_id}'",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "task_id": result.task_id,
                            "comment_id": result.id,
                            "comment": result.comment,
                            "created_at": result.created_at,
                            "updated_at": result.updated_at,
                        },
                    }
                ),
                201,
            )
