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
        profile_image = author.profile_image
        profile_image.save()
        author.save()
        return author
