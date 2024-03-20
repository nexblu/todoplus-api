from itsdangerous.url_safe import URLSafeSerializer, Serializer
from config import reset_password_key


class Misc:
    @staticmethod
    async def get_reset_token(email):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        token = s.dumps({"email": email})
        return token

    @staticmethod
    async def verify_reset_token(token):
        s = URLSafeSerializer(reset_password_key, salt="reset_password")
        try:
            s.loads(token)["email"]
        except:
            return None
        else:
            return s.loads(token)
