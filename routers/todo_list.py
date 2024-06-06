from flask import Blueprint, request, jsonify
from databases import TodolistCRUD
from utils import token_required, TaskNotFound
import datetime
import traceback
from sqlalchemy.exc import IntegrityError, DataError

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
                    "message": f"data '{user.username!r}' was found",
                    "result": {
                        "task": [
                            {
                                "user_id": author.id,
                                "username": author.username,
                                "task_id": todo_list.id,
                                "task": todo_list.task,
                                "date": todo_list.date,
                                "tags": todo_list.tags,
                                "is_done": todo_list.is_done,
                                "is_pin": todo_list.is_pin,
                                "bookmark": todo_list.bookmark,
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
                    "message": f"task {user.username!r} not found",
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
                    "message": f"data '{user.username!r}' was found",
                    "result": {
                        "task": {
                            "user_id": author.id,
                            "username": author.username,
                            "task_id": todo_list.id,
                            "task": todo_list.task,
                            "date": todo_list.date,
                            "tags": todo_list.tags,
                            "is_done": todo_list.is_done,
                            "is_pin": todo_list.is_pin,
                            "bookmark": todo_list.bookmark,
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
        await todo_list_database.delete(
            "task_id", user_id=user.id, task_id=task_id, email=user.email
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
                    "status_code": 200,
                    "message": f"success delete task {user.username!r} with id '{task_id}'",
                }
            ),
            200,
        )


@todo_list_router.put("/todoplus/v1/todolist/is-done")
@token_required()
async def todo_list_update_is_done():
    data = request.json
    user = request.user
    is_done = data.get("is_done")
    try:
        await todo_list_database.update(
            "is-done", user_id=user.id, is_done=is_done, email=user.email
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
                    "message": f"success update mark task {user.username!r}",
                }
            ),
            201,
        )


@todo_list_router.get("/todoplus/v1/todolist/is-done")
@token_required()
async def todo_list_get_is_done():
    user = request.user
    try:
        data = await todo_list_database.get("is-done", user_id=user.id)
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
                    "message": f"data '{user.username!r}' was found",
                    "result": {
                        "task": [
                            {
                                "user_id": author.id,
                                "username": author.username,
                                "task_id": todo_list.id,
                                "task": todo_list.task,
                                "date": todo_list.date,
                                "tags": todo_list.tags,
                                "is_done": todo_list.is_done,
                                "is_pin": todo_list.is_pin,
                                "bookmark": todo_list.bookmark,
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
