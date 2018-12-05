"""
    warriorbeat/api/post/schema.py
    Schema for Post Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.post.model import Article


class PostSchema(Schema):
    """Generic Post Schema"""
    postId = fields.Str()
    title = fields.Str()
    date = fields.Str()
    type = fields.Str()


class ArticleSchema(PostSchema):
    """Article Post Type Schema"""

    author = fields.Pluck('AuthorSchema', 'authorId')
    cover_image = fields.Pluck('ImageSchema', 'mediaId')
    content = fields.Str()
    categories = fields.Pluck('CategorySchema', 'categoryId', many=True)

    @post_load
    def make_article(self, data):
        """return article instance"""
        article = Article.create_or_update(**data)
        article.schema = ArticleSchema()
        return article
