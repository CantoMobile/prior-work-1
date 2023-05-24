import os
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError
from config.config import ProductionConfig, DevelopmentConfig
import hashlib


class AuthService:
    def __init__(self):
        if os.environ.get('FLASK_ENV') == 'development':
            self.secret_key = DevelopmentConfig.SECRET_KEY
        else:
            self.secret_key = ProductionConfig.SECRET_KEY

    def generate_auth_token(self, user):
        payload = {
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
        }
        token = jwt.encode(payload, self.secret_key,
                           algorithm="HS256")
        return {"token": token}

    def verify_auth_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            print(payload)
            user_email = payload['email']
            return user_email
        except InvalidTokenError as e:
            print("Invalid token" + e.message)
            return {"error": e.message}

    def encrypt(self, text):
        sha256 = hashlib.sha256()
        text_bytes = text.encode('utf-8')
        sha256.update(text_bytes)
        hash_result = sha256.hexdigest()

        return hash_result

    
