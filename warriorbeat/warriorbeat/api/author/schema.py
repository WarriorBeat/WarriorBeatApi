"""
    warriorbeat/api/author/schema.py
    Schema for Author Resource
"""

from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

from warriorbeat.api.author.model import Author

ma = Marshmallow()


class AuthorSchema(ma.Schema):
    """Author Schema"""
    class Meta:
        strict = True
    authorId = fields.Str()
    name = fields.Str()
    profile_image = fields.Nested('ProfileImageSchema', exclude=('profile', ))
    posts = fields.Nested('ArticleSchema', many=True, exclude=('author', ))
    title = fields.Str()
    description = fields.Str()

    @post_load
    def make_author(self, data):
        author = Author.create_or_retrieve(**data)
        author.schema = AuthorSchema()
        return author
