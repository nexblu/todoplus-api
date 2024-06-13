from flask import Blueprint, request
from controllers import LoginService

login_router = Blueprint("api user login", __name__)
login_service = LoginService()


@login_router.post("/todoplus/v1/user/login")
async def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    return await login_service.login(email, password)
