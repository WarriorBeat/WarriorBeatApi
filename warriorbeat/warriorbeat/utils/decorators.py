"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

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
        def wrapper(self, *args, **kwargs):
            try:
                data = schema.load(request.json)
            except Exception as e:
                print(e)
                data = schema.loads(request.json)
            f_return = func(self, data, *args, **kwargs)
            if dump:
                return schema.dumps(f_return)
            return f_return
        return wrapper
    return decorator
