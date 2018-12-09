"""
    warriorbeat/api/author/view.py
    View for Author Resource
"""

from flask_restful import Resource

from warriorbeat.api.author.model import Author
from warriorbeat.api.author.schema import AuthorSchema
from warriorbeat.utils import (allow_relations, parse_json, retrieve_item,
                               use_schema)


class AuthorList(Resource):

    def get(self):
        return Author.all()

    @use_schema(AuthorSchema(), dump=True)
    def post(self, author):
        author.save()
        return author


class AuthorItem(Resource):

    @retrieve_item(Author, AuthorSchema)
    @allow_relations
    def get(self, author, data, **kwargs):
        return data

    @parse_json
    @retrieve_item(Author, AuthorSchema)
    def patch(self, data, author, **kwargs):
        author = author.update(data)
        return author.save()

    @retrieve_item(Author, AuthorSchema)
    def delete(self, article, **kwargs):
        article.delete()
        return '', 204
