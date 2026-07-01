import jwt
from datetime import datetime, timedelta
from app.config import Config

class JwtService:

    @staticmethod
    def generate_token(user_id):

        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return token

    @staticmethod
    def verify_token(token):

        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"]
            )

            return payload

        except jwt.ExpiredSignatureError:
            return None

        except jwt.InvalidTokenError:
            return None