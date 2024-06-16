from flask import Blueprint, request
from controllers import LoginController

login_router = Blueprint("api user login", __name__)
login_service = LoginController()


@login_router.post("/todoplus/v1/user/login")
async def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return await login_service.login(username, password)
