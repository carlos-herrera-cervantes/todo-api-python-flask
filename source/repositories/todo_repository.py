from bson.objectid import ObjectId
from json import loads
from bson.json_util import dumps

from models.config import Config
from models.todo import Todo
from serializers.common_serializer import default
from modules.mongodb_module import build_lookup_filter, build_paginate_filter, build_sort_filter
from modules.common_module import parse_pages, get_type_ordering_object

Config.start_connection()

def get_all(query_param, filter={}):
    """
    Return all todos
    Parameters
    ----------
    query_params: dict
        Dictionary with query params of request
    filter: dict
        Dictionary with properties used to filter
    """
    pages = parse_pages(query_params)
    sort = query_params.get('sort', '-created_at')
    exists_with = query_params.get('with')
    
    if not exists_with:
        todos = Todo.objects(__raw__=filter).order_by(sort).skip(pages['page']).limit(pages['page_size']).to_json()
        return loads(todos, object_hook=default)

    partial_pipeline = build_lookup_filter(exists_with, 'todo')
    type_sort = get_type_ordering_object(sort)
    partial_pipeline = build_sort_filter(type_sort, partial_pipeline)

    if pages['page'] > 0:
        partial_pipeline = build_paginate_filter(pages['page'], pages['page_size'], partial_pipeline)
    
    partial_pipeline.append({ '$unwind': '$user' })
    todos = Todo.objects(__raw__=filter).aggregate(*partial_pipeline)

    return loads(dumps(todos), object_hook=default)

def get_by_id(id):
    """
    Return a specific todo
    Parameters
    ----------
    id: string
        The specific todo ID to retrieve
    query_params: dict
        Dictionary with query params of request
    """
    todo = Todo.objects.get(id=ObjectId(id))
    return loads(todo.to_json(), object_hook=default)

def get_by_id_with_populate(id, references):
    """
    Return a specific todo with references fields
    Parameters
    ----------
    id: string
        The specific todo ID to retrieve
    references: str
        String that indicates the collections must be populated
    """
    pipeline = build_lookup_filter(references, 'todo')
    pipeline.append({ '$match': { '_id': ObjectId(id) } })
    todos = Todo.objects().aggregate(*pipeline)
    return loads(dumps(todos), object_hook=default)

def count(filter={}):
    """
    Return total of documents
    Parameters
    ----------
    filter: dict
        The specific todo criteria to count
    """
    return Todo.objects(__raw__=filter).count()