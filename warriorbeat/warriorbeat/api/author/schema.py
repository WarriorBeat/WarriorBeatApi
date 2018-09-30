"""
    warriorbeat/api/author/schema.py
    Schema for Author Resource
"""

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import AbsoluteUrlFor, Hyperlinks
from marshmallow import fields, post_load

from warriorbeat.api.author.model import Author


ma = Marshmallow()


class AuthorSchema(ma.Schema):
    class Meta:
        strict = True
    authorId = fields.Str()
    name = fields.Str()
    avatar = fields.Str()
    posts = fields.List(fields.Str())
    title = fields.Str()
    description = fields.Str()

    @post_load
    def make_author(self, data):
        print(data)
        return Author(**data)
