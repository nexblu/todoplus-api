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
    if username and task:
        try:
            await db_todo_list.insert(username, task, created_at, is_done)
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
                    "result": "bad request",
                }
            ),
            404,
        )


@todo_list_router.put("/todoplus/v1/todolist")
async def todo_list_update():
    data = request.json
    username = data.get("username")
    id = data.get("id")
    category = data.get("category")
    is_done = data.get("is_done")
    new_task = data.get("new_task")
    user = await db_user.get("username", username=username)
    if user:
        try:
            id = int(id)
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
            task_id = await db_todo_list.get("id", username=username, id=id)
            if task_id:
                if category in ("task", "is_done"):
                    if category == "task":
                        await db_todo_list.update(
                            "id", username=username, id=id, new_task=new_task
                        )
                    elif category == "is_done":
                        try:
                            is_done = bool(is_done)
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
                            await db_todo_list.update(
                                "id", username=username, id=id, is_done=is_done
                            )
                    return jsonify(
                        {
                            "result": f"success update to id : {id} | [{category}]",
                            "status_code": 200,
                        },
                        200,
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
            else:
                return (
                    jsonify(
                        {
                            "status_code": 404,
                            "result": "bad request",
                        }
                    ),
                    404,
                )
    else:
        return (
            jsonify(
                {
                    "status_code": 404,
                    "result": "bad request",
                }
            ),
            404,
        )
