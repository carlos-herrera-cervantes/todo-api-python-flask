from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId

from managers import todo_manager
from repositories import todo_repository
from decorators.user_decorator import exists_user
from decorators.todo_decorator import exists_todo, validate_todo
from decorators.common_decorator import authorize_request, validate_role, validate_pagination
from models.role import Role

todo_router = Blueprint('todo_router', __name__)

@todo_router.route('/api/v1/users/<id>/todos', methods=['GET'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@validate_pagination
@exists_user
def get_all(id):
    result = todo_repository.get_all(request.args, { 'user': ObjectId(id) })
    return jsonify({ 'status': True, 'data': result })

@todo_router.route('/api/v1/users/<id>/todos/<todo_id>', methods=['GET'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
@exists_todo
def get_by_id(id, todo_id):
    result = todo_repository.get_by_id(todo_id)
    return jsonify({ 'status': True, 'data': result })

@todo_router.route('/api/v1/users/<id>/todos', methods=['POST'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
@validate_todo
def create(id):
    todo = request.json
    todo['user'] = id
    result = todo_manager.create(todo)
    return jsonify({ 'status': True, 'data': result }), 201

@todo_router.route('/api/v1/users/<id>/todos/<todo_id>', methods=['PATCH'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
@exists_todo
def update_by_id(id, todo_id):
    result = todo_manager.update_by_id(todo_id, request.json)
    return jsonify({ 'status': True, 'data': result })

@todo_router.route('/api/v1/users/<id>/todos/<todo_id>', methods=['DELETE'])
@authorize_request
@validate_role([Role.ADMIN.value, Role.CLIENT.value])
@exists_user
@exists_user
def delete_by_id(id, todo_id):
    todo_manager.delete_by_id(todo_id)
    return jsonify({ 'status': True, 'data': {} }), 204