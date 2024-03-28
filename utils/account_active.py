from itsdangerous.url_safe import URLSafeSerializer
from config import account_active_key


class AccountActiveToken:
    @staticmethod
    async def get_token(email):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        token = s.dumps({"email": email})
        return token

    @staticmethod
    async def verify_token(token):
        s = URLSafeSerializer(account_active_key, salt="account_active")
        try:
            s.loads(token)["email"]
        except:
            return None
        else:
            return s.loads(token)
