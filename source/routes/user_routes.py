from flask import Blueprint, request, jsonify

from managers import user_manager
from repositories import user_repository
from decorators.user_decorator import exists_user, validate_user, encode_password
from decorators.common_decorator import authorize_request, validate_pagination, validate_role
from models.role import Role
from modules.user_module import delete_todo_by_user

user_router = Blueprint('user_router', __name__)

@user_router.route('/api/v1/users', methods=['GET'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@validate_pagination
def get_all():
    result = user_repository.get_all(request.args)
    return jsonify({ 'status': True, 'data': result })

@user_router.route('/api/v1/users/<id>', methods=['GET'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
def get_by_id(id):
    result = user_repository.get_by_id(id)
    return jsonify({ 'status': True, 'data': result })

@user_router.route('/api/v1/users', methods=['POST'])
@validate_user
def create():
    result = user_manager.create(request.json)
    return jsonify({ 'status': True, 'data': result }), 201

@user_router.route('/api/v1/users/<id>', methods=['PATCH'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
@encode_password
def update_by_id(id):
    result = user_manager.update_by_id(id, request.json)
    return jsonify({ 'status': True, 'data': result })

@user_router.route('/api/v1/users/<id>', methods=['DELETE'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
def delete_by_id(id):
    user_manager.delete_by_id(id)
    delete_todo_by_user(id)
    return jsonify({ 'status': True, 'data': {} }), 204