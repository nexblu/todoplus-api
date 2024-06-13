from flask import Blueprint, request
from utils import token_required
from controllers import IsDoneController

todo_list_is_done_router = Blueprint("api user task mark as done", __name__)
is_done_controller = IsDoneController()


@todo_list_is_done_router.delete("/todoplus/v1/todolist/is-done")
@token_required()
async def delete_todo_list_is_done():
    user = request.user
    return await is_done_controller.delete_is_done(user)


@todo_list_is_done_router.post("/todoplus/v1/todolist/is-done")
@token_required()
async def post_todo_list_is_done():
    user = request.user
    return await is_done_controller.add_is_done(user)


@todo_list_is_done_router.get("/todoplus/v1/todolist/is-done")
@token_required()
async def todo_list_get_is_done():
    user = request.user
    return await is_done_controller.get_is_done(user)


@todo_list_is_done_router.post("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_post_is_done(task_id):
    user = request.user
    return await is_done_controller.add_is_done_by_id(user, task_id)


@todo_list_is_done_router.delete("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_delete_is_done_task_id(task_id):
    user = request.user
    return await is_done_controller.delete_is_done_by_id(user, task_id)


@todo_list_is_done_router.get("/todoplus/v1/todolist/is-done/<int:task_id>")
@token_required()
async def todo_list_get_is_done_task_id(task_id):
    user = request.user
    return await is_done_controller.get_is_done_by_id(user, task_id)
