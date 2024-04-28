from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from config import account_active_key
import datetime


class AccountActive(Token):
    @staticmethod
    async def insert(email):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        token = s.dumps(
            {
                "email": email,
                "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            }
        )
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        try:
            s.loads(token)["email"]
            s.loads(token)["created_at"]
        except:
            return None
        else:
            return s.loads(token)
