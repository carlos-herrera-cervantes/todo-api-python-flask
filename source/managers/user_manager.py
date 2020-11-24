from json import loads
from bson.objectid import ObjectId

from models.config import Config
from models.user import User
from serializers.common_serializer import default

Config.start_connection()

def create(user):
    """
    Create a new user
    Parameters
    ----------
    user: dict
        User dictionary
    """
    return loads(User(**user).save().to_json(), object_hook=default)

def update_by_id(user_id, user):
    """
    Update a specific user
    Parameters
    ----------
    user_id: string
        The user ID to update
    user: dict
        User object to update
    """
    User.objects(id=ObjectId(user_id)).update_one(**user)
    updated_user = User.objects.get(id=ObjectId(user_id))
    updated_user.save()
    return loads(updated_user.to_json(), object_hook=default)

def delete_by_id(user_id):
    """
    Delete a specific user
    Parameters
    ----------
    user_id: string
        The user ID to delete
    """
    User.objects(id=ObjectId(user_id)).delete()
    return True