from dotenv import load_dotenv
import os

load_dotenv()

debug_mode = os.getenv("DEBUG")
database_url = os.getenv("DB_URL")
jwt_key = os.getenv("JWT_KEY")
algorithm = os.getenv("ALGORITHM")
