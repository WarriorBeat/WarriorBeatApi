"""
    warriorbeat/api/post/schema.py
    Schema for Post Resource
"""

from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import AbsoluteUrlFor, Hyperlinks
from marshmallow import fields, post_load

from warriorbeat.api.post.model import Article
from warriorbeat.api.author.schema import AuthorSchema

ma = Marshmallow()


class ArticleSchema(ma.Schema):
    """Article Schema"""
    class Meta:
        strict = True
    postId = fields.Str()
    title = fields.Str()
    author = fields.Nested('AuthorSchema', only=('authorId', 'name'))
    type = fields.Str()
    cover_image = fields.Str()
    content = fields.Str()

    @post_load
    def make_article(self, data):
        return Article(**data)
