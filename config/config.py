from dotenv import load_dotenv
import os

load_dotenv()

debug_mode = os.environ.get("DEBUG")
mongodb_url = os.environ.get("MONGODB_URL")
postgresql_url = os.environ.get("POSTGRESQL_URL")
