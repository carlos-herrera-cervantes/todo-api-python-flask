from bson.objectid import ObjectId

from managers import user_manager, todo_manager
from repositories import user_repository

def add_todo_to_user(user_id, todo_id):
    """
    Add todo ID into the todos of user
    Parameters
    ----------
    user_id: str
        User ID
    todo_id: str
        ToDo ID
    """
    user = user_repository.get_by_id(user_id)
    todo_ids = user['todos']
    todo_ids.append(todo_id)
    todos = { 'todos': todo_ids }
    user_manager.update(user_id, todos)

def delete_todo_of_user(user_id, todo_id):
    """
    Remove the ID of ToDo from the user's ToDos
    Parameters
    ----------
    user_id: str
        User ID
    todo_id: str
        ToDo ID
    """
    user = user_repository.get_by_id(user_id)
    todo_ids = user['todos']
    todo_ids.remove(todo_id)
    todos = { 'todos': todo_ids }
    user_manager.update(user_id, todos)

def delete_todo_by_user(user_id):
    """
    Delete all ToDo's of user
    Parameters
    ----------
    user_id: str
        User ID
    """
    todo_manager.delete_many({ 'user': ObjectId(user_id) })