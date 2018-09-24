"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

from functools import wraps


def use_schema(schema):
    """
    @use_schema : @decorator
    Serialize data for get requests

    params:
    schema: instance
        Instance of schema to utilize
    func: object
        function to wrap
        must return data to be serialized
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            _data = func(self, *args, **kwargs)
            data = schema.dump(_data)
            return data
        return wrapper
    return decorator
