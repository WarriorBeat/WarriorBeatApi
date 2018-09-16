"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

from functools import wraps
from slugify import slugify
from datetime import datetime
from flask import url_for, redirect


def post_modify(date=False):
    """
    Modify data in a post request.

    params:
    func: object
        function to wrap
        required func to return at least dict of values
    date: bool
        Append date to data.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data, return_func = func(*args, **kwargs)
            if date:
                now = datetime.now()
                now = datetime.strftime(now, '%Y-%m-%d T %H:%M:%S')
                data['date'] = now
            return return_func(data)
        return wrapper
    return decorator
