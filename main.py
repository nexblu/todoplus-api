from flask import Flask
from flask_cors import CORS
from config import debug_mode
from routers.login import login_router
from routers.user import user_router

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(login_router)
app.register_blueprint(user_router)


if __name__ == "__main__":
    app.run(debug=debug_mode)
