"""
    warriorbeat/api/author/view.py
    View for Author Resource
"""

from flask_restful import Resource, request
from webargs.flaskparser import use_args
from warriorbeat.api.author.schema import AuthorSchema


class AuthorList(Resource):

    def get(self):
        return ''

    def post(self):
        author = AuthorSchema().loads(request.json).data
        print(author)
        data = AuthorSchema().dumps(author)
        return data
