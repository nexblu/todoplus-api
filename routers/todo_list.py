from flask import Blueprint, request, jsonify
from databases import TodolistDatabase, UserDatabase

todo_list_router = Blueprint("api user task", __name__)
db_todo_list = TodolistDatabase()
db_user = UserDatabase()


@todo_list_router.post("/todoplus/v1/todolist")
async def todo_list_add():
    data = request.json
    username = data.get("username")
    task = data.get("task")
    created_at = data.get("created_at")
    is_done = data.get("is_done")
    try:
        result = await db_todo_list.insert(username, task, created_at, is_done)
    except:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": "bad request",
                }
            ),
            400,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 201,
                    "result": f"success created with task id => {result.id!r}",
                }
            ),
            201,
        )


@todo_list_router.delete("/todoplus/v1/todolist")
async def todo_list_delete():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    task = await db_todo_list.get("id", username=username, id=id)
    if task:
        await db_todo_list.delete("task", username=username, id=id)
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": f"success delete todo {id!r}",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"task {id!r} not found",
                }
            ),
            404,
        )


@todo_list_router.get("/todoplus/v1/todolist/<string:username>")
async def todo_list_get(username):
    user = await db_user.get("username", username=username)
    if user:
        result = await db_todo_list.get("username", username=username)
        todo_lists = [
            {
                "id": todo_list.id,
                "username": todo_list.username,
                "task": todo_list.task,
                "is_done": todo_list.is_done,
                "created_at": todo_list.created_at,
            }
            for todo_list in result
        ]
        return jsonify({"result": todo_lists, "status_code": 200}, 200)
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"user {username!r} not found",
                }
            ),
            404,
        )


@todo_list_router.put("/todoplus/v1/todolist/is_done")
async def todo_list_update_is_done():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    is_done = data.get("is_done")
    task = await db_todo_list.get("id", username=username, id=id)
    if task:
        await db_todo_list.update("is_done", username=username, id=id, is_done=is_done)
        return (
            jsonify(
                {
                    "status_code": 200,
                    "result": f"success change todo {id!r}",
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": f"task {id!r} not found",
                }
            ),
            404,
        )
