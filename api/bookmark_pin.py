from flask import Blueprint, request
from utils import token_required
from controllers import BookmarkPinController

bookmark_pinned_router = Blueprint("api user task bookmark pinned", __name__)
bookmark_pin_controller = BookmarkPinController()


@bookmark_pinned_router.post(
    "/todoplus/v1/todolist/bookmark/bookmark-pin/<int:task_id>/<int:bookmark_id>"
)
@token_required()
async def post_bookmark_pinned_task_id(task_id, bookmark_id):
    user = request.user
    return await bookmark_pin_controller.add_bookmark_pin_by_id(
        user, task_id, bookmark_id
    )


@bookmark_pinned_router.delete(
    "/todoplus/v1/todolist/bookmark/bookmark-pin/<int:task_id>/<int:bookmark_id>"
)
@token_required()
async def delete_bookmark_pinned_task_id(task_id, bookmark_id):
    user = request.user
    return await bookmark_pin_controller.delete_bookmark_pin_by_id(
        user, task_id, bookmark_id
    )


@bookmark_pinned_router.get(
    "/todoplus/v1/todolist/bookmark/bookmark-pin/<int:task_id>/<int:bookmark_id>"
)
@token_required()
async def get_bookmark_pinned_task_id(task_id, bookmark_id):
    user = request.user
    return await bookmark_pin_controller.get_bookmark_pin_by_id(
        user, task_id, bookmark_id
    )
