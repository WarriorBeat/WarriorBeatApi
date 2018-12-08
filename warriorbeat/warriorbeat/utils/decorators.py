"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

import json
from functools import wraps

from flask_restful import request


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
            is_many = type(request.json) == list and allow_many
            try:
                data = schema.load(request.json, many=is_many)
            except Exception as e:
                print(e)
                try:
                    data = schema.loads(request.json, many=is_many)
                except Exception as e:
                    print(e)
                    raise
            data = [data] if allow_many and type(data) != list else data
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
            if schema:
                item = model.retrieve(item_id, schema=schema, instance=True)
            else:
                item = model.retrieve(item_id)
            if item is None and raise_404:
                return '', 404
            args = args + (item, )
            return func(*args, **kwargs)
        return wrapper
    return decorator
