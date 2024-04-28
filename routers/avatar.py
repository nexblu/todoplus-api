from flask import Blueprint, jsonify, request, render_template

avatar_router = Blueprint("api avatar", __name__)


@avatar_router.post("/todoplus/v1/user/avatar")
async def avatar_post():
    pass


@avatar_router.get("/todoplus/v1/user/avatar/<string:username>")
async def avatar_get(username):
    pass
