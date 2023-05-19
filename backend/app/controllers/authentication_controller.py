from flask import request, jsonify, abort
from models.auth_token_model import AuthToken
from models.user_model import User
from services.auth_service import AuthService
from . import auth_bp
from repositories.authentication_repository import AuthenticationRepository
from repositories.user_repository import UserRepository

auth_repo = AuthenticationRepository()
user_repo = UserRepository()


@auth_bp.route('/auth', methods=['POST'])
def auth():
    data = request.json
    user = user_repo.find_by_email(data['email'])
    if user and User.verify_password(user, data['password']):
        token = AuthService.generate_auth_token(user)
        auth_token = {'user': user['_id'], 'token': token}
        AuthToken.validate(auth_token)  # Validar los campos requeridos
        auth_token = auth_repo.save(auth_token)
        return auth_token
    else:
        abort(401)


@auth_bp.route('/auth/<token>', methods=['DELETE'])
def logout(token):
    token = auth_repo.find_by_token(token)
    if token:
        auth_repo.delete_by_token(token)
        return '', 204
    else:
        abort(404)
