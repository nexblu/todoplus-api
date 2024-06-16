from flask import Blueprint, request
from utils import token_required
from controllers import TaskPinController

todo_list_pinned_router = Blueprint("api user task pinned", __name__)
is_pin_controller = TaskPinController()


@todo_list_pinned_router.get("/todoplus/v1/todolist/task-pinned")
@token_required()
async def todo_list_get_is_pin():
    user = request.user
    return await is_pin_controller.get_is_pin(user)


@todo_list_pinned_router.delete("/todoplus/v1/todolist/task-pinned")
@token_required()
async def todo_list_delete_is_pin():
    user = request.user
    return await is_pin_controller.delete_is_pin(user)


@todo_list_pinned_router.post("/todoplus/v1/todolist/task-pinned")
@token_required()
async def todo_list_post_is_pin():
    user = request.user
    return await is_pin_controller.add_is_pin(user)


@todo_list_pinned_router.post("/todoplus/v1/todolist/task-pinned/<int:task_id>")
@token_required()
async def todo_list_post_is_pin_task_id(task_id):
    user = request.user
    return await is_pin_controller.add_is_pin_by_id(user, task_id)


@todo_list_pinned_router.delete("/todoplus/v1/todolist/task-pinned/<int:task_id>")
@token_required()
async def todo_list_delete_is_pin_task_id(task_id):
    user = request.user
    return await is_pin_controller.delete_is_pin_by_id(user, task_id)


@todo_list_pinned_router.get("/todoplus/v1/todolist/task-pinned/<int:task_id>")
@token_required()
async def todo_list_get_is_pin_task_id(task_id):
    user = request.user
    return await is_pin_controller.get_is_pin_by_id(user, task_id)
