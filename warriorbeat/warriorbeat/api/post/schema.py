"""
    warriorbeat/api/post/schema.py
    Schema for Post Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.post.model import Article


class PostSchema(Schema):
    """Generic Post Schema"""
    postId = fields.Str(required=True)
    title = fields.Str(required=True)
    date = fields.Str()
    type = fields.Str()


class ArticleSchema(PostSchema):
    """Article Post Type Schema"""
    author = fields.Nested('AuthorSchema', exclude=(
        'posts', ), load_only=True)
    authorId = fields.Pluck('AuthorSchema', 'authorId',
                            attribute='author', dump_only=True)
    cover_image = fields.Nested('CoverImageSchema')
    content = fields.Str(required=True)
    categories = fields.Nested('CategorySchema', many=True)

    @post_load
    def make_article(self, data):
        """return article instance"""
        article = Article.create_or_update(**data)
        article.schema = ArticleSchema()
        return article
