"""
    warriorbeat/api/post/schema.py
    Schema for Post Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.post.model import Article


class ArticleSchema(Schema):
    """Article Schema"""
    postId = fields.Str(required=True)
    title = fields.Str(required=True)
    author = fields.Nested('AuthorSchema', exclude=('posts', ), required=True)
    type = fields.Str()
    cover_image = fields.Nested('CoverImageSchema')
    content = fields.Str(required=True)

    @post_load
    def make_article(self, data):
        """return article instance"""
        article = Article.create_or_retrieve(**data)
        article.schema = ArticleSchema()
        return article
