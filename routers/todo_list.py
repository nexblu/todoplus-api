from flask import Blueprint, request, jsonify
from databases import TodolistDatabase

todo_list_router = Blueprint("api user task", __name__)
db = TodolistDatabase()


@todo_list_router.post("/todoplus/v1/todolist")
async def todo_list_add():
    data = request.json
    username = data.get("username")
    task = data.get("task")
    if username and task:
        try:
            await db.insert(username, task)
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
                        "result": "success created",
                    }
                ),
                201,
            )
    else:
        return (
            jsonify(
                {
                    "status_code": 400,
                    "result": "bad request",
                }
            ),
            400,
        )


@todo_list_router.get("/todoplus/v1/todolist/<string:username>")
async def todo_list_get(username):
    result = await db.get("username", username=username)
    todo_lists = [
        (
            todo_list.task,
            todo_list.username,
            todo_list.is_done,
            todo_list.id,
            todo_list.created_at,
        )
        for todo_list in result
    ]
    return jsonify({"result": todo_lists, "status_code": 200}, 200)
