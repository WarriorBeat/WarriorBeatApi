"""
    warriorbeat/api/author/view.py
    View for Author Resource
"""

from flask_restful import Resource

from warriorbeat.api.author.model import Author
from warriorbeat.api.author.schema import AuthorSchema
from warriorbeat.utils import use_schema


class AuthorList(Resource):

    def get(self):
        return Author.all()

    @use_schema(AuthorSchema(), dump=True)
    def post(self, author):
        author.save()
        return author


class AuthorItem(Resource):

    def get(self, authorId):
        author = Author.retrieve(authorId)
        return author
