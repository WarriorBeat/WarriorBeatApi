"""
    warriorbeat/api/author/schema.py
    Schema for Author Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.author.model import Author


class AuthorSchema(Schema):
    """Author Schema"""
    authorId = fields.Str(required=True)
    name = fields.Str()
    profile_image = fields.Nested('ProfileImageSchema')
    posts = fields.Nested('ArticleSchema', many=True,
                          exclude=('author', ))
    title = fields.Str()
    description = fields.Str(
        required=False, allow_none=True, default='Staff Member')

    @post_load
    def make_author(self, data):
        author = Author.create_or_retrieve(**data)
        author.schema = AuthorSchema()
        return author
