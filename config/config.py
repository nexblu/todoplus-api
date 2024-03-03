from dotenv import load_dotenv
import os

load_dotenv()

debug_mode = os.environ.get("DEBUG")
database_url = os.environ.get("DB_URL")
jwt_key = os.environ.get("JWT_KEY")
algorithm = os.environ.get("ALGORITHM")
