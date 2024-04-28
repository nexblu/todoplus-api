from flask import Blueprint, request, jsonify
from databases import TodolistDatabase
from utils import token_required
from sqlalchemy import exc
import models
import databases

todo_list_router = Blueprint("api user task", __name__)
todo_list_database = TodolistDatabase()


@todo_list_router.post("/todoplus/v1/todolist")
@token_required()
async def todo_list_add():
    data = request.json
    username = data.get("username")
    task = data.get("task")
    tags = data.get("tags")
    date = data.get("date")
    try:
        await todo_list_database.insert(username, task, tags, date)
    except models.todo_list.MaxTags5:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"max tags is 5",
                }
            ),
            400,
        )
    except exc.IntegrityError:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    except (
        models.todo_list.UsernameRequired,
        models.todo_list.TaskRequired,
        models.todo_list.TagsList,
    ):
        return (
            jsonify(
                {
                    "status_code": 400,
                    "message": f"data is invalid",
                }
            ),
            400,
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


@todo_list_router.delete("/todoplus/v1/todolist/id")
@token_required()
async def todo_list_delete():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    try:
        await todo_list_database.delete("task", username=username, id=id)
    except:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"task {id} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success delete task with id {id!r}",
                }
            ),
            201,
        )


@todo_list_router.delete("/todoplus/v1/todolist")
@token_required()
async def todo_list_clear():
    data = request.json
    username = data.get("username")
    try:
        await todo_list_database.delete("username", username=username)
    except:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"success clear task {username!r}",
                }
            ),
            201,
        )


@todo_list_router.get("/todoplus/v1/todolist/<string:username>")
@token_required()
async def todo_list_get(username):
    if result := await todo_list_database.get("username", username=username):
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "tags": todo_list.tags,
                "date": todo_list.date,
                "update_at": todo_list.update_at,
                "created_at": todo_list.created_at,
                "is_pin": todo_list.is_pin,
                "bookmark": todo_list.bookmark,
                "is_done": todo_list.is_done,
            }
            for todo_list in result
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": todo_lists,
                    "message": f"data {username!r} has been found",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": [],
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )


@todo_list_router.get("/todoplus/v1/todolist/pinned/<string:username>")
@token_required()
async def todo_list_get_pinned(username):
    if result := await todo_list_database.get("pinned", username=username):
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "tags": todo_list.tags,
                "date": todo_list.date,
                "update_at": todo_list.update_at,
                "created_at": todo_list.created_at,
                "is_pin": todo_list.is_pin,
                "bookmark": todo_list.bookmark,
                "is_done": todo_list.is_done,
            }
            for todo_list in result
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": todo_lists,
                    "message": f"data {username!r} has been found",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": [],
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )


@todo_list_router.get("/todoplus/v1/todolist/bookmark/<string:username>")
@token_required()
async def todo_list_get_bookmark(username):
    if result := await todo_list_database.get("bookmark", username=username):
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "tags": todo_list.tags,
                "date": todo_list.date,
                "update_at": todo_list.update_at,
                "created_at": todo_list.created_at,
                "is_pin": todo_list.is_pin,
                "bookmark": todo_list.bookmark,
                "is_done": todo_list.is_done,
            }
            for todo_list in result
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": todo_lists,
                    "message": f"data {username!r} has been found",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": [],
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )


@todo_list_router.get("/todoplus/v1/todolist/completed/<string:username>")
@token_required()
async def todo_list_get_completed(username):
    if result := await todo_list_database.get("completed", username=username):
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "tags": todo_list.tags,
                "date": todo_list.date,
                "update_at": todo_list.update_at,
                "created_at": todo_list.created_at,
                "is_pin": todo_list.is_pin,
                "bookmark": todo_list.bookmark,
                "is_done": todo_list.is_done,
            }
            for todo_list in result
        ]
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": todo_lists,
                    "message": f"data {username!r} has been found",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": [],
                    "message": f"user {username!r} not found",
                }
            ),
            404,
        )


@todo_list_router.get("/todoplus/v1/todolist/incomplete/<string:username>")
@token_required()
async def todo_list_get_incomplete(username):
    if result := await todo_list_database.get("incomplete", username=username):
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "tags": todo_list.tags,
                "date": todo_list.date,
                "update_at": todo_list.update_at,
                "created_at": todo_list.created_at,
                "is_pin": todo_list.is_pin,
                "bookmark": todo_list.bookmark,
                "is_done": todo_list.is_done,
            }
            for todo_list in result
        ]
        return (
            jsonify({"status_code": 200, "message": todo_lists}),
            200,
        )
    else:
        return (
            jsonify({"status_code": 404, "message": f"user {username!r} not found"}),
            404,
        )


@todo_list_router.put("/todoplus/v1/todolist/is_done")
@token_required()
async def todo_list_update_is_done():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    try:
        await todo_list_database.update(
            "is_done",
            username=username,
            id=id,
        )
    except:
        return (
            jsonify({"status_code": 404, "message": f"task {id} not found"}),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"succes update task {id}",
                }
            ),
            201,
        )


@todo_list_router.put("/todoplus/v1/todolist/bookmark")
@token_required()
async def todo_list_update_bookmark():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    try:
        result = await todo_list_database.update(
            "bookmark",
            username=username,
            id=id,
        )
    except:
        return (
            jsonify({"status_code": 404, "message": f"task {id} not found"}),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": {"bookmark": result.bookmark},
                    "message": f"succes update task {id}",
                }
            ),
            201,
        )


@todo_list_router.delete("/todoplus/v1/todolist/tags")
@token_required()
async def todo_list_remove_tags():
    data = request.json
    tags = data.get("tags")
    username = data.get("username")
    id = data.get("id")
    try:
        await todo_list_database.delete("tags", username=username, id=id, tags=tags)
    except databases.todo_list.InvalidTags:
        return (
            jsonify({"status_code": 404, "message": f"invalid tags"}),
            404,
        )
    except Exception:
        return (
            jsonify({"status_code": 400, "message": f"bad request"}),
            400,
        )
    else:
        return (
            jsonify(
                {"status_code": 201, "message": f"success delete tags from tags {id}"}
            ),
            201,
        )


@todo_list_router.put("/todoplus/v1/todolist/task")
@token_required()
async def todo_list_update_task():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    new_task = data.get("new_task")
    try:
        await todo_list_database.update(
            "task",
            username=username,
            id=id,
            new_task=new_task,
        )
    except:
        return (
            jsonify({"status_code": 404, "message": f"task {id} not found"}),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"succes update task {id} to {new_task!r}",
                }
            ),
            201,
        )


@todo_list_router.put("/todoplus/v1/todolist/pinned")
@token_required()
async def todo_list_update_pinned():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    try:
        await todo_list_database.update(
            "pinned",
            username=username,
            id=id,
        )
    except databases.todo_list.MaxPinned3:
        return (
            jsonify({"status_code": 400, "message": f"max pinned is 3"}),
            400,
        )
    except databases.todo_list.TaskNotFoundError:
        return (
            jsonify({"status_code": 404, "message": f"task {id} not found"}),
            404,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "message": f"succes update task {id}",
                }
            ),
            201,
        )
