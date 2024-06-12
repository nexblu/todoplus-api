from flask import Blueprint, request, jsonify
from repository import TodoListCRUD, IsDoneCRUD, IsPinCRUD, BookmarkCRUD
from utils import token_required, TaskNotFound
import datetime
from sqlalchemy.exc import IntegrityError, DataError

todo_list_router = Blueprint("api user task", __name__)
todo_list_database = TodoListCRUD()
is_done_database = IsDoneCRUD()
is_pin_database = IsPinCRUD()
bookmark_database = BookmarkCRUD()


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
            task,
            tags,
            datetime.datetime.now(datetime.timezone.utc).timestamp(),
        )
    except (IntegrityError, DataError):
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"data is invalid",
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


@todo_list_router.get("/todoplus/v1/todolist")
@token_required()
async def todo_list_get():
    user = request.user
    try:
        data = await todo_list_database.get(
            "all",
            user_id=user.id,
        )
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
                                "is_done": await is_done_database.get(
                                    "is_done", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_done_id": await is_done_database.get(
                                    "is_done_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
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
                            for author, todo_list in data
                        ],
                    },
                }
            ),
            200,
        )


@todo_list_router.delete("/todoplus/v1/todolist")
@token_required()
async def todo_list_delete():
    user = request.user
    try:
        await todo_list_database.delete(
            "clear",
            user_id=user.id,
            email=user.email,
        )
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
                    "message": f"success clear task",
                }
            ),
            201,
        )


@todo_list_router.get("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_get_task_id(task_id):
    user = request.user
    try:
        data = await todo_list_database.get("task_id", user_id=user.id, task_id=task_id)
    except TaskNotFound:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"task '{task_id}' not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        author, todo_list = data
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
                            "is_done": await is_done_database.get(
                                "is_done", task_id=todo_list.id, user_id=author.id
                            ),
                            "is_done_id": await is_done_database.get(
                                "is_done_id", task_id=todo_list.id, user_id=author.id
                            ),
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


@todo_list_router.delete("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_delete_task_id(task_id):
    user = request.user
    try:
        await todo_list_database.delete("task_id", user_id=user.id, task_id=task_id)
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
                    "status_code": 200,
                    "message": f"success delete task {user.username!r} with id '{task_id}'",
                }
            ),
            200,
        )


@todo_list_router.put("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_put_task_id(task_id):
    user = request.user
    data = request.json
    new_task = data.get("new_task")
    try:
        await todo_list_database.update(
            "new_task", user_id=user.id, task_id=task_id, new_task=new_task
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
                    "status_code": 200,
                    "message": f"success update task {user.username!r} with id '{task_id}'",
                }
            ),
            200,
        )


@todo_list_router.get("/todoplus/v1/todolist/is-pin")
@token_required()
async def todo_list_get_is_pin():
    user = request.user
    try:
        data = await is_pin_database.get("all", user_id=user.id)
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
                                "is_done": await is_done_database.get(
                                    "is_done", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_done_id": await is_done_database.get(
                                    "is_done_id",
                                    task_id=todo_list.id,
                                    user_id=author.id,
                                ),
                                "is_pin": await is_pin_database.get(
                                    "is_pin", task_id=todo_list.id, user_id=author.id
                                ),
                                "is_pin_id": pinned.id,
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
                            for author, todo_list, pinned in data
                        ],
                    },
                }
            ),
            200,
        )


@todo_list_router.delete("/todoplus/v1/todolist/is-pin")
@token_required()
async def todo_list_delete_is_pin():
    user = request.user
    try:
        await is_pin_database.delete("all", user_id=user.id)
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
                    "message": f"success clear bookmark {user.username!r}",
                }
            ),
            201,
        )


@todo_list_router.post("/todoplus/v1/todolist/is-pin")
@token_required()
async def todo_list_post_is_pin():
    user = request.user
    try:
        await is_pin_database.update("all", user_id=user.id)
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
                    "message": f"success pinned all task {user.username!r}",
                }
            ),
            201,
        )


@todo_list_router.post("/todoplus/v1/todolist/is-pin/<int:task_id>")
@token_required()
async def todo_list_post_is_pin_task_id(task_id):
    user = request.user
    try:
        await is_pin_database.insert(user.id, task_id)
    except IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"task '{task_id}' already pinned",
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
                    "message": f"success pinned task '{task_id}'",
                }
            ),
            201,
        )


@todo_list_router.delete("/todoplus/v1/todolist/is-pin/<int:task_id>")
@token_required()
async def todo_list_delete_is_pin_task_id(task_id):
    user = request.user
    try:
        await is_pin_database.delete("task_id", user_id=user.id, task_id=task_id)
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
                    "message": f"success remove pinned '{task_id}'",
                }
            ),
            201,
        )


@todo_list_router.get("/todoplus/v1/todolist/is-pin/<int:task_id>")
@token_required()
async def todo_list_get_is_pin_task_id(task_id):
    user = request.user
    try:
        result = await is_pin_database.get("task_id", user_id=user.id, task_id=task_id)
    except TaskNotFound:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"task '{task_id}' not found",
                    "result": None,
                }
            ),
            404,
        )
    else:
        author, todo_list, pinned = result
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
                            "is_done": await is_done_database.get(
                                "is_done", task_id=todo_list.id, user_id=author.id
                            ),
                            "is_done_id": await is_done_database.get(
                                "is_done_id", task_id=todo_list.id, user_id=author.id
                            ),
                            "is_pin": await is_pin_database.get(
                                "is_pin", task_id=todo_list.id, user_id=author.id
                            ),
                            "is_pin_id": pinned.id,
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
