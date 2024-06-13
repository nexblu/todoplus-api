from flask import Blueprint, request
from utils import token_required
from controllers import CommentController

todo_list_comment_router = Blueprint("api user task comment", __name__)
comment_controller = CommentController()


@todo_list_comment_router.post("/todoplus/v1/todolist/comment/<int:task_id>")
@token_required()
async def todo_list_post_bookmark(task_id):
    data = request.json
    user = request.user
    comment = data.get("comment")
    return await comment_controller.add_comment(user, comment, task_id)


@todo_list_comment_router.get("/todoplus/v1/todolist/comment/<int:task_id>")
@token_required()
async def todo_list_get_bookmark_by_task_id(task_id):
    user = request.user
    return await comment_controller.get_comment_by_task_id(user, task_id)


@todo_list_comment_router.delete("/todoplus/v1/todolist/comment/<int:task_id>")
@token_required()
async def todo_list_delete_bookmark_by_task_id(task_id):
    user = request.user
    return await comment_controller.clear_comment_by_task_id(user, task_id)
