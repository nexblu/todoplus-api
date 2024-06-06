from dotenv import load_dotenv
import os

load_dotenv()

debug_mode = os.environ.get("DEBUG")
mongodb_url = os.environ.get("MONGODB_URL")
postgresql_url = os.environ.get("POSTGRESQL_URL")
smtp_email = os.environ.get("SMTP_EMAIL")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_port = os.environ.get("SMTP_PORT")
smtp_server = os.environ.get("SMTP_SERVER")
account_active_key = os.environ.get("ACCOUNT_ACTIVE_KEY")
reset_password_key = os.environ.get("RESET_PASSWORD_KEY")
access_token_key = os.environ.get("ACCESS_TOKEN_KEY")
refresh_token_key = os.environ.get("REFRESH_TOKEN_KEY")
algorithm = os.environ.get("ALGORITHM")
api_url = os.environ.get("API_URL")
todoplus_url = os.environ.get("TODOPLUS_URL")
