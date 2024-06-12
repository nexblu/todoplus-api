from flask import Flask
from flask_cors import CORS
from config import debug_mode, mongodb_url
from repository import db_session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils import (
    handle_404,
    handle_415,
    handle_429,
    handle_400,
    handle_401,
    handle_403,
    handle_405,
)
from api.register import register_router
from api.login import login_router
from api.todo_list import todo_list_router
from api.account_active import account_active_router
from api.refresh_token import refresh_token_router

app = Flask(__name__)
CORS(app, supports_credentials=True)
limiter = Limiter(
    get_remote_address, app=app, default_limits=[""], storage_uri=mongodb_url
)


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.teardown_appcontext
async def shutdown_session(exception=None):
    db_session.remove()


@app.teardown_request
async def checkin_db(exception=None):
    db_session.remove()


app.register_blueprint(register_router)
app.register_blueprint(login_router)
app.register_blueprint(todo_list_router)
app.register_blueprint(account_active_router)
app.register_blueprint(refresh_token_router)

app.register_error_handler(429, handle_429)
app.register_error_handler(404, handle_404)
app.register_error_handler(415, handle_415)
app.register_error_handler(400, handle_400)
app.register_error_handler(401, handle_401)
app.register_error_handler(403, handle_403)
app.register_error_handler(405, handle_405)


if __name__ == "__main__":
    app.run(debug=debug_mode)
