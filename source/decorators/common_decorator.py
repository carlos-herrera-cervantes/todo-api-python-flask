from functools import wraps
from bson.json_util import dumps
from jwt import decode
from flask import request, jsonify

from locales.translations import get_text
from models.key_translation import KeyTranslation
from settings import SECRET_KEY

def authorize_request(fn):
    """
    Validates token of request
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        response_invalid_token = { 
            'status': False,
            'code': KeyTranslation.INVALID_TOKEN.value,
            'message': get_text(request.headers, KeyTranslation.INVALID_TOKEN.value)
        }

        try:
            token = request.headers.get('Authorization')

            if token is None:
                return jsonify(response_invalid_token), 401

            decode(token.split(' ').pop(), SECRET_KEY, algorithms=['HS256'])
            return fn(*args, **kwargs)
        except Exception:
            return jsonify(response_invalid_token), 401
    return inner

def validate_pagination(fn):
    """
    Validates pagination params
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        paginate = request.args.get('paginate')
        page = request.args.get('page')
        page_size = request.args.get('page_size')

        if not paginate:
            return fn(*args, **kwargs)

        if paginate and (not page or not page_size):
            return jsonify(
                { 
                    'status': False,
                    'code': KeyTranslation.MISSING_PAGINATE_PARAMS.value,
                    'message': get_text(request.headers, KeyTranslation.MISSING_PAGINATE_PARAMS.value)
                }), 400

        if int(page) < 1 or int(page_size) < 1 or int(page_size) > 100:
            return jsonify(
                { 
                    'status': False,
                    'code': KeyTranslation.INVALID_PAGINATION.value,
                    'message': get_text(request.headers, KeyTranslation.INVALID_PAGINATION.value)
                })

        return fn(*args, **kwargs)
    return inner

def validate_role(roles):
    """
    Validates role of user
    Parameters
    ----------
    roles: array
        Roles which this operation admits
    """
    def wrapped(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            token = request.headers.get('Authorization')
            payload = decode(token.split(' ').pop(), SECRET_KEY, algorithms=['HS256'])
            role = payload['role']

            if role not in roles:
                return jsonify(
                    { 
                        'status': False,
                        'code': KeyTranslation.INVALID_PERMISSIONS.value,
                        'message': get_text(request.headers, KeyTranslation.INVALID_PERMISSIONS.value)
                    })
            
            return fn(*args, **kwargs)
        return inner
    return wrapped