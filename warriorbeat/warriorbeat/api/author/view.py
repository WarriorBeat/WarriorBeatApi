"""
    warriorbeat/api/author/view.py
    View for Author Resource
"""

from flask_restful import Resource, request

from warriorbeat.api.author.model import Author
from warriorbeat.api.author.schema import AuthorSchema


class AuthorList(Resource):

    def get(self):
        return Author.all()

    def post(self):
        author = AuthorSchema().loads(request.json).data
        author.save()
        data = AuthorSchema().dumps(author)
        return data
