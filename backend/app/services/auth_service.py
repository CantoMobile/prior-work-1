import os
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError
from app.config.config import ProductionConfig, DevelopmentConfig
import hashlib
from app.services.role_service import extract_permissions
from app.utils.logger import logger


class AuthService:
    def __init__(self):
        if os.environ.get('FLASK_ENV') == 'development':
            self.secret_key = DevelopmentConfig.SECRET_KEY
        else:
            self.secret_key = ProductionConfig.SECRET_KEY

    def generate_auth_token(self, user, role_id):
        logger.info('Generating auth token for user %s', user["email"])
        permissions = extract_permissions(role_id)
        payload = {
            'email': user['email'],
            'permissions': list(permissions),
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expires in 1 day
        }
        token = jwt.encode(payload, self.secret_key,
                           algorithm="HS256")
        return {"token": token}

    def verify_auth_token(self, token):
        logger.info("Verifying auth token")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_email = payload['email']
            permissions = payload['permissions']
            set_list = set(tuple(permission) for permission in permissions)
            return user_email, set_list
        except InvalidTokenError as e:
            logger.error("Invalid token" + e.message)
            return {"error": e.message}

    def encrypt(self, text):
        sha256 = hashlib.sha256()
        text_bytes = text.encode('utf-8')
        sha256.update(text_bytes)
        hash_result = sha256.hexdigest()

        return hash_result
