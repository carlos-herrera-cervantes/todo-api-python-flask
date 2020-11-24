from flask import Blueprint, request, jsonify
from jwt import encode
from datetime import datetime, timedelta

from decorators.user_decorator import exists_user
from repositories import user_repository
from settings import SECRET_KEY
from decorators.user_decorator import validate_credentials

auth_router = Blueprint('auth_router', __name__)

@auth_router.route('/api/v1/auth', methods=['POST'])
@validate_credentials
def login():
    email = request.json.get('email', '')
    user = user_repository.get_one({ 'email': email })
    token = encode({ 'email': email, 'role': user['role'], 'exp': datetime.utcnow() + timedelta(days=7) }, SECRET_KEY, algorithm='HS256')
    return jsonify({ 'status': True, 'data': token.decode('ascii') })