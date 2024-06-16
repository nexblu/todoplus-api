from flask import Blueprint, request
from utils import token_required
from controllers import TaskController

todo_list_router = Blueprint("api user task", __name__)
task_service = TaskController()


@todo_list_router.post("/todoplus/v1/todolist")
@token_required()
async def todo_list_add():
    data = request.json
    user = request.user
    task = data.get("task")
    description = data.get("description")
    tags = data.get("tags")
    return await task_service.add_task(user, task, description, tags)


@todo_list_router.get("/todoplus/v1/todolist")
@token_required()
async def todo_list_get():
    user = request.user
    return await task_service.get_task(user)


@todo_list_router.delete("/todoplus/v1/todolist")
@token_required()
async def todo_list_delete():
    user = request.user
    return await task_service.delete_task(user)


@todo_list_router.get("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_get_task_id(task_id):
    user = request.user
    return await task_service.get_task_by_id(user, task_id)


@todo_list_router.delete("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_delete_task_id(task_id):
    user = request.user
    return await task_service.delete_task_by_id(user, task_id)


@todo_list_router.put("/todoplus/v1/todolist/<int:task_id>")
@token_required()
async def todo_list_put_task_id(task_id):
    user = request.user
    data = request.json
    new_task = data.get("new_task")
    return await task_service.put_task_by_id(user, task_id, new_task)
