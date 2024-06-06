from flask import Blueprint, request, jsonify
from databases import TodolistCRUD
from utils import token_required
import datetime
import traceback

todo_list_router = Blueprint("api user task", __name__)
todo_list_database = TodolistCRUD()


@todo_list_router.post("/todoplus/v1/todolist")
@token_required()
async def todo_list_add():
    data = request.json
    user = request.user
    task = data.get("task")
    tags = data.get("tags")
    try:
        await todo_list_database.insert(
            user.id,
            user.email,
            task,
            tags,
            datetime.datetime.now(datetime.timezone.utc).timestamp(),
        )
    except Exception:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"bad request",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success create task {task!r}",
                }
            ),
            201,
        )
