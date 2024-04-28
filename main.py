from flask import Flask, jsonify
from flask_cors import CORS
from config import debug_mode
from routers.login import login_router
from routers.user import user_router
from routers.todo_list import todo_list_router
from routers.register import register_router
from routers.reset_password import reset_router
from routers.account_active import account_active_router
from routers.email import email_router
from databases import db_session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import handle_404, handle_415, handle_429, handle_400
from flask_github import GitHub

app = Flask(__name__)
CORS(app, supports_credentials=True)
limiter = Limiter(
    get_remote_address, app=app, default_limits=[""], storage_uri="memory://"
)
app.config["GITHUB_CLIENT_ID"] = "XXX"
app.config["GITHUB_CLIENT_SECRET"] = "YYY"
app.config["GITHUB_BASE_URL"] = "https://HOSTNAME/api/v3/"
app.config["GITHUB_AUTH_URL"] = "https://HOSTNAME/login/oauth/"

github = GitHub(app)


app.register_blueprint(login_router)
app.register_blueprint(user_router)
app.register_blueprint(todo_list_router)
app.register_blueprint(register_router)
app.register_blueprint(reset_router)
app.register_blueprint(account_active_router)
app.register_blueprint(email_router)
app.register_error_handler(429, handle_429)
app.register_error_handler(404, handle_404)
app.register_error_handler(415, handle_415)
app.register_error_handler(400, handle_400)


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.teardown_appcontext
async def shutdown_session(exception=None):
    db_session.remove()


@app.get("/")
async def home():
    return jsonify("welcome to todolist api"), 200


if __name__ == "__main__":
    app.run(debug=debug_mode)
