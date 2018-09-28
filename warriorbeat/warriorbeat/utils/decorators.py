"""
    warriorbeat/api/utils/decorators.py
    Useful decorators with various functions
"""

from functools import wraps

import requests
from flask_restful import request, url_for


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


def forward_resource(**kwargs):
    """
    @forward_resource : @decorator
    forwards data from one endpoint to another via redirect

    kwargs:
    data: dict, json
        specify payload to forward
        defaults to returned value of wrapped function
    headers: dict
        specify additional headers to request
        defaults to current request content_type
    method: string
        specify HTTP method used to forward
        defaults to post
    endpoint: string
        specify endpoint to forward to
        defaults to wrapped functions self.target attr 

    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args):
            _payload = func(self, *args)
            payload = kwargs.get('data', _payload)
            _headers = {'Content-Type': request.content_type}
            headers = kwargs.get('headers', _headers)
            method = kwargs.get('method', 'post').lower()
            target = self.target or kwargs.pop('endpoint')
            url = url_for(target, _external=True)
            _request = getattr(requests, method)
            req = _request(url, data=payload, headers=headers)
            return req.json()
        return wrapper
    return decorator
