from flask import Blueprint, request, jsonify
from repository import TodoListCRUD, IsDoneCRUD, IsPinCRUD, BookmarkCRUD
from utils import token_required, TaskNotFound
from sqlalchemy.exc import IntegrityError

todo_list_is_done_router = Blueprint("api user task mark as done", __name__)
todo_list_database = TodoListCRUD()
is_done_database = IsDoneCRUD()
is_pin_database = IsPinCRUD()
bookmark_database = BookmarkCRUD()


@todo_list_is_done_router.delete("/todoplus/v1/todolist/is-done")
@token_required()
async def delete_todo_list_is_done():
    user = request.user
    try:
        await is_done_database.delete("all", user_id=user.id)
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
                    "message": f"success update mark task {user.username!r}",
                }
            ),
            201,
        )


@todo_list_is_done_router.post("/todoplus/v1/todolist/is-done")
@token_required()
async def post_todo_list_is_done():
    user = request.user
    try:
        await is_done_database.update("all", user_id=user.id)
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
                    "message": f"success mark all task {user.username!r}",
                }
            ),
            201,
        )


@todo_list_is_done_router.get("/todoplus/v1/todolist/is-done")
@token_required()
async def todo_list_get_is_done():
    user = request.user
    try:
        data = await is_done_database.get("all", user_id=user.id)
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
                                "is_done": True,
                                "is_done_id": is_done.id,
                                "is_pin": await is_pin_database.get(
                                    "is_pin", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_pin_id": await is_pin_database.get(
                                    "is_pin_id", task_id=todo_list.id, user_id=author.id
                                ),
                                "bookmark": await bookmark_database.get(
                                    "bookmark", task_id=todo_list.id, user_id=author.id
                                ),
                                "bookmark_id": await bookmark_database.get(
                                    "bookmark_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "updated_at": todo_list.updated_at,
                                "created_at": todo_list.created_at,
                            }
                            for author, todo_list, is_done in data
                        ],
                    },
                }
            ),
            200,
        )


@todo_list_is_done_router.post("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_post_is_done(task_id):
    user = request.user
    try:
        await is_done_database.insert(user.id, task_id)
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"task '{task_id}' already mark done",
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
                    "message": f"success mark '{task_id}' as done",
                }
            ),
            201,
        )


@todo_list_is_done_router.delete("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_delete_is_done_task_id(task_id):
    user = request.user
    try:
        await is_done_database.delete("task_id", user_id=user.id, task_id=task_id)
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
                    "message": f"success unmark '{task_id}' as done",
                }
            ),
            201,
        )


@todo_list_is_done_router.get("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_get_is_done_task_id(task_id):
    user = request.user
    try:
        result = await is_done_database.get("task_id", user_id=user.id, task_id=task_id)
    except TaskNotFound:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"task {user.username!r} not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        author, todo_list, is_done = result
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
                            "is_done": True,
                            "is_done_id": is_done.id,
                            "is_pin": await is_pin_database.get(
                                "is_pin", task_id=todo_list.id, user_id=author.id
                            ),
                            "is_pin_id": await is_pin_database.get(
                                "is_pin_id", task_id=todo_list.id, user_id=author.id
                            ),
                            "bookmark": await bookmark_database.get(
                                "bookmark", task_id=todo_list.id, user_id=author.id
                            ),
                            "bookmark_id": await bookmark_database.get(
                                "bookmark_id", task_id=todo_list.id, user_id=author.id
                            ),
                            "updated_at": todo_list.updated_at,
                            "created_at": todo_list.created_at,
                        }
                    },
                }
            ),
            200,
        )
