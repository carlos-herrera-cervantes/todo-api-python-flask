from bson.objectid import ObjectId
from json import loads
from bson.json_util import dumps

from models.config import Config
from models.user import User
from serializers.common_serializer import default
from modules.mongodb_module import build_lookup_filter, build_paginate_filter, build_sort_filter
from modules.common_module import parse_pages, get_type_ordering_object

Config.start_connection()

def get_all(query_params):
    """
    Return all users
    Parameters
    ----------
    query_params: dict
        Dictionary with query params of request
    """
    pages = parse_pages(query_params)
    sort = query_params.get('sort', '-created_at')
    exists_with = query_params.get('with')

    if not exists_with:
        users = User.objects().order_by(sort).skip(pages['page']).limit(pages['page_size']).to_json()
        return loads(users, object_hook=default)

    partial_pipeline = build_lookup_filter(exists_with, 'user')
    type_sort = get_type_ordering_object(sort)
    partial_pipeline = build_sort_filter(type_sort, partial_pipeline)
    
    if pages['page'] > 0:
        partial_pipeline = build_paginate_filter(pages['page'], pages['page_size'], partial_pipeline)

    users = User.objects().aggregate(*partial_pipeline)
    
    return loads(dumps(users), object_hook=default)

def get_by_id(id):
    """
    Return a specific user
    Parameters
    ----------
    id: string
        The specific user ID to retrieve
    """
    user = User.objects.get(id=ObjectId(id))
    return loads(user.to_json(), object_hook=default)

def get_by_id_with_populate(id, references):
    """
    Return a specific user with references fields
    Parameters
    ----------
    id: string
        The specific user ID to retrieve
    references: str
        String that indicates the collections must be populated
    """
    pipeline = build_lookup_filter(references, 'user')
    pipeline.append({ '$match': { '_id': ObjectId(id) } })
    users = User.objects().aggregate(*pipeline)
    return loads(dumps(users), object_hook=default)

def get_one(filter):
    """
    Return a specific user by criteria
    Parameters
    ----------
    filter: dict
        The specific user criteria to retrieve
    """
    user = User.objects(__raw__=filter).first()
    return user

def get_one_with_populate(filter, references):
    """
    Return a specific user by criteria
    Parameters
    ----------
    filter: dict
        The specific user criteria to retrieve
    references: str
        String that indicates the collections must be populated
    """
    pipeline = build_lookup_filter(references, 'user')
    pipeline.append({ '$match': filter })
    user = User.objects().aggregate(*pipeline)
    return loads(dumps(user), object_hook=default)

def count(filter={}):
    """
    Return total of documents
    Parameters
    ----------
    filter: dict
        The specific user criteria to count
    """
    return User.objects(__raw__=filter).count()