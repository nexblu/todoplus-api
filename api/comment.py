from flask import Blueprint, request
from utils import token_required
from controllers import CommentController

todo_list_comment_router = Blueprint("api user task comment", __name__)
comment_controller = CommentController()


@todo_list_comment_router.post("/todoplus/v1/todolist/comment")
@token_required()
async def todo_list_post_bookmark():
    data = request.json
    user = request.user
    comment = data.get("comment")
    task_id = data.get("task_id")
    return await comment_controller.add_comment(user, comment, task_id)


@todo_list_comment_router.get("/todoplus/v1/todolist/comment")
@token_required()
async def todo_list_get_bookmark():
    user = request.user
    return await comment_controller.get_comment(user)
