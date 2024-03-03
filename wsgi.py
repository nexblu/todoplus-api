from app import app
from config import debug_mode


if __name__ == "__main__":
    app.run(debug=debug_mode)
