from flask import Flask
from flask_cors import CORS
from config import debug_mode
from routers.login import login_router
from routers.user import user_router
from routers.todo_list import todo_list_router
from routers.register import register_router
from routers.email import email_router
from databases import db_session

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(login_router)
app.register_blueprint(user_router)
app.register_blueprint(todo_list_router)
app.register_blueprint(register_router)
app.register_blueprint(email_router)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.get("/")
def home():
    return "welcome to todoplus api"


if __name__ == "__main__":
    app.run(debug=debug_mode)
