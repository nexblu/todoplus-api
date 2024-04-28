from .token import Token
from itsdangerous.url_safe import URLSafeSerializer
from config import reset_password_key
import datetime


class TokenResetPassword(Token):
    @staticmethod
    async def insert(email):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        token = s.dumps(
            {
                "email": email,
                "created_at": datetime.datetime.now(datetime.timezone.utc).timestamp(),
            }
        )
        return token

    @staticmethod
    async def get(token):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        try:
            s.loads(token)["email"]
            s.loads(token)["created_at"]
        except:
            return None
        else:
            return s.loads(token)
