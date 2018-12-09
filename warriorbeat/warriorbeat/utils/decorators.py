"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

import json
from functools import wraps

from flask_restful import request

from .utils import get_json_load_method


def use_schema(schema, dump=False, allow_many=False):
    """
    @use_schema : @decorator
    Se/Deserialize data for post requests

    args:
    schema: instance
        Instance of schema to utilize
    func: object
        function to wrap
        must return data to be serialized

    kwargs:
    dump: bool
        Dump return data to the schema
    allow_many: bool
        allow list of items to be loaded
        will always return a list

    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            load_method, json_type = get_json_load_method(schema, request.json)
            is_many = json_type is list and allow_many
            data = load_method(request.json, many=is_many)
            data = data if allow_many and json_type != list else data
            args = args + (data, )
            f_return = func(*args, **kwargs)
            if dump:
                return schema.dumps(f_return, many=is_many)
            return f_return
        return wrapper
    return decorator


def parse_json(func):
    """
    @parse_json : @decorator
    Deserialize json data if needed

    returns:
        decorated function with additional
        parsed_data keyword
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        data_type = type(data)
        data = json.loads(data) if data_type == str else data
        args = args + (data, )
        f_return = func(*args, **kwargs)
        return f_return
    return wrapper


def retrieve_item(model, schema=None, raise_404=True):
    """
    @retrieve_item : @decorator
    Attempts to retrieve item from endpoint id kwarg

    args:
    model: object (class)
        resource model to retrieve item with
    func: object
        function to wrap

    kwargs:
    schema: object (instance)
        schema to be passed to model
    raise_404: bool
        whether to raise 404 if item is not found

    returns:
        404 if item does not exist
        instance if item exists and schema is passed
        item if only model is passed
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            item_id = next(iter(kwargs.values()))
            item = model.retrieve(item_id)
            if item is None and raise_404:
                return '', 404
            if schema:
                _item = model.retrieve(item_id)
                item = schema().load(_item) if _item is not None else None
            args = args + (item, )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def allow_relations(func):
    """
    @allow_relations : @decorator
    Parses 'include' query arg and populates relations

    returns:
        item data with any relations populated entirely
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        item = args[-1]
        query = request.args.get('include', None)
        data = item.schema.dump(item)
        if query:
            query = query.split(',')
            relations = {k: v for k, v in [
                item.get_relation(r) for r in query] if v is not None}
            data = {**data, **relations}
        args = args + (data, )
        return func(*args, **kwargs)
    return wrapper
