from flask import Blueprint, request
from utils import token_required
from controllers import BookmarkController

todo_list_bookmark_router = Blueprint("api user task bookmark", __name__)
bookmark_service = BookmarkController()


@todo_list_bookmark_router.get("/todoplus/v1/todolist/bookmark")
@token_required()
async def todo_list_get_bookmark():
    user = request.user
    return await bookmark_service.get_bookmark(user)


@todo_list_bookmark_router.delete("/todoplus/v1/todolist/bookmark")
@token_required()
async def todo_list_delete_bookmark():
    user = request.user
    return await bookmark_service.delete_bookmark(user)


@todo_list_bookmark_router.post("/todoplus/v1/todolist/bookmark")
@token_required()
async def todo_list_post_bookmark():
    user = request.user
    return await bookmark_service.add_bookmark(user)


@todo_list_bookmark_router.post("/todoplus/v1/todolist/bookmark/<int:task_id>")
@token_required()
async def todo_list_post_bookmark_task_id(task_id):
    user = request.user
    return await bookmark_service.add_bookmark_by_id(user, task_id)


@todo_list_bookmark_router.delete("/todoplus/v1/todolist/bookmark/<int:task_id>")
@token_required()
async def todo_list_delete_bookmark_task_id(task_id):
    user = request.user
    return await bookmark_service.delete_bookmark_by_id(user, task_id)


@todo_list_bookmark_router.get("/todoplus/v1/todolist/bookmark/<int:task_id>")
@token_required()
async def todo_list_get_bookmark_task_id(task_id):
    user = request.user
    return await bookmark_service.get_bookmark_by_id(user, task_id)
