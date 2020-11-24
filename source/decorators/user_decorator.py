from flask import request, jsonify
from functools import wraps
from bson.json_util import dumps, loads
from mongoengine.errors import DoesNotExist, ValidationError
from bcrypt import checkpw, hashpw, gensalt

from repositories import user_repository
from locales.translations import get_text
from models.key_translation import KeyTranslation
from models.user import User

def exists_user(fn):
    """
    Validates if user exists in the collection
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            id = kwargs['id']
            user_repository.get_by_id(id)
            return fn(*args, **kwargs)
        except DoesNotExist:
            return jsonify(
                { 
                    'status': False,
                    'code': KeyTranslation.USER_NOT_FOUND.value,
                    'message': get_text(request.headers, KeyTranslation.USER_NOT_FOUND.value)
                }), 404
    return inner

def validate_user(fn):
    """
    Validates fields of user
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            user = User(**request.json)
            user.validate()
            return fn(*args, **kwargs)
        except ValidationError as ex:
            dict = ex.__dict__
            errors = ''

            for key, value in dict['errors'].items():
                errors += f'\n {key} {value} \n'

            return jsonify(
                {
                    'status': False,
                    'code': KeyTranslation.USER_NOT_VALID.value,
                    'message': get_text(request.headers, KeyTranslation.USER_NOT_VALID.value) + ': ' + errors
                })
    return inner

def validate_credentials(fn):
    """
    Validates credentials of user
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        response_not_found_user = { 
            'status': False,
            'code': KeyTranslation.USER_NOT_FOUND.value,
            'message': get_text(request.headers, KeyTranslation.USER_NOT_FOUND.value)
        }

        try:
            email = request.json.get('email', '')
            password_sended = request.json.get('password', '')
            user = user_repository.get_one({ 'email': email })
            password_retrieved = user['password']
            
            if checkpw(password_sended.encode('utf-8'), password_retrieved.encode('utf-8')):
                return fn(*args, **kwargs)

            return jsonify(
                { 
                    'status': False, 
                    'code': KeyTranslation.WRONG_CREDENTIALS.value,
                    'message': get_text(request.headers, KeyTranslation.WRONG_CREDENTIALS.value)
                }), 400
        except DoesNotExist:
            return jsonify(response_not_found_user), 404
    return inner

def encode_password(fn):
    """
    If there is a password property in the body of the request, it will be encoded
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        exists_password = request.json.get('password')

        if not exists_password:
            return fn(*args, **kwargs)

        hashed_password = hashpw(exists_password.encode('utf-8'), gensalt())
        request.json['password'] = hashed_password.decode('utf-8')
        return fn(*args, **kwargs)

    return inner