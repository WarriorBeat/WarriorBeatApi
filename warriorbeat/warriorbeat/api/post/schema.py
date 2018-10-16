"""
    warriorbeat/api/post/schema.py
    Schema for Post Resource
"""

from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

from warriorbeat.api.post.model import Article

ma = Marshmallow()


class ArticleSchema(ma.Schema):
    """Article Schema"""
    class Meta:
        strict = True
    postId = fields.Str()
    title = fields.Str()
    author = fields.Nested('AuthorSchema', exclude=('posts', ))
    type = fields.Str()
    cover_image = fields.Nested('CoverImageSchema', exclude=('post', ))
    content = fields.Str()

    @post_load
    def make_article(self, data):
        """return article instance"""
        article = Article.create_or_retrieve(**data)
        article.schema = ArticleSchema()
        return article
