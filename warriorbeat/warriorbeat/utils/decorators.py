"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

import json
from functools import wraps

from flask_restful import request


def use_schema(schema, dump=False):
    """
    @use_schema : @decorator
    Se/Deserialize data for post requests

    params:
    schema: instance
        Instance of schema to utilize
    dump: bool
        Dump return data to the schema
    func: object
        function to wrap
        must return data to be serialized
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = schema.load(request.json)
            except Exception as e:
                print(e)
                try:
                    data = schema.loads(request.json)
                except Exception as e:
                    print(e)
                    raise
            args = args + (data, )
            f_return = func(*args, **kwargs)
            if dump:
                return schema.dumps(f_return)
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
