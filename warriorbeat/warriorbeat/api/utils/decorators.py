"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

from datetime import datetime
from functools import wraps
from flask import redirect, url_for
from flask_restful import abort
from slugify import slugify
from warriorbeat.api.exceptions import ItemAlreadyExists


def post_modify(date=False):
    """
    @post_modify : @decorator
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


def validate_unique(item):
    """
    @validate_unique : @decorator
    Checks given item from data for uniqueness

    params:
    func: object
        function to wrap
    item: string
        Item name to check in dictionary
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = self.parse.parse_args()
            database = getattr(self, 'db')
            check = data[item]
            if database.exists(check):
                raise ItemAlreadyExists(check)
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator
