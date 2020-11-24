from flask import request, jsonify
from functools import wraps
from bson.json_util import dumps, loads
from mongoengine.errors import DoesNotExist, ValidationError

from repositories import todo_repository
from locales.translations import get_text
from models.key_translation import KeyTranslation
from models.todo import Todo

def exists_todo(fn):
    """
    Validates if todo exists in the collection
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            id = kwargs['todo_id']
            todo_repository.get_by_id(id)
            return fn(*args, **kwargs)
        except DoesNotExist:
            return jsonify(
                { 
                    'status': False,
                    'code': KeyTranslation.TODO_NOT_FOUND.value,
                    'message': get_text(request.headers, KeyTranslation.TODO_NOT_FOUND.value)
                }), 404
    return inner

def validate_todo(fn):
    """
    Validates fields of todo
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            todo = Todo(**request.json)
            todo.validate()
            return fn(*args, **kwargs)
        except ValidationError as ex:
            dict = ex.__dict__
            errors = ''

            for key, value in dict['errors'].items():
                errors += f'\n {key} {value} \n'

            return jsonify(
                {
                    'status': False,
                    'code': KeyTranslation.TODO_NOT_VALID.value,
                    'message': get_text(request.headers, KeyTranslation.TODO_NOT_VALID.value) + ': ' + errors
                })
    return inner