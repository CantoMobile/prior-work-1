from datetime import datetime, timedelta
import jwt


class AuthService:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_auth_token(self, user):
        payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(days=1)  # El token expira en 1 día
        }
        token = jwt.encode(payload, self.secret_key,
                           algorithm='HS256').decode('utf-8')
        return token
