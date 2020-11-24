from json import loads
from bson.objectid import ObjectId

from models.config import Config
from models.todo import Todo
from serializers.common_serializer import default

Config.start_connection()

def create(todo):
    """
    Create a new todo
    Parameters
    ----------
    todo: dict
        Todo dictionary
    """
    return loads(Todo(**todo).save().to_json(), object_hook=default)

def update_by_id(todo_id, todo):
    """
    Update a specific todo
    Parameters
    ----------
    todo_id: string
        The todo ID to update
    todo: dict
        Todo object to update
    """
    Todo.objects(id=ObjectId(todo_id)).update_one(**todo)
    updated_todo = Todo.objects.get(id=ObjectId(todo_id))
    updated_todo.save()
    return loads(updated_todo.to_json(), object_hook=default)

def delete_by_id(todo_id):
    """
    Delete a specific todo
    Parameters
    ----------
    todo_id: string
        The todo ID to delete
    """
    Todo.objects(id=ObjectId(todo_id)).delete()
    return True

def delete_many(filter):
    """
    Delete todos by specific filter
    Parameters
    ----------
    filter: dict
        Properties specifying the filter to apply
    """
    Todo.objects(__raw__=filter).delete()
    return True