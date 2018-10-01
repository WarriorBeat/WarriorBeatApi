"""
    warriorbeat/api/author/view.py
    View for Author Resource
"""

from flask_restful import Resource, request
from warriorbeat.api.author.schema import AuthorSchema


class AuthorList(Resource):

    def get(self):
        pass

    def post(self):
        author = AuthorSchema().loads(request.json).data
        print(author)
        author.save()
        data = AuthorSchema().dumps(author)
        return data
