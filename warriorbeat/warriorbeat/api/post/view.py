"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource

from warriorbeat.api.post.model import Article
from warriorbeat.api.post.schema import ArticleSchema
from warriorbeat.utils import parse_json, retrieve_item, use_schema


class PostList(Resource):

    def get(self):
        return Article.all()

    @use_schema(ArticleSchema(), dump=True)
    def post(self, article):
        article.create()
        return article


class PostItem(Resource):

    @retrieve_item(Article)
    def get(self, article, **kwargs):
        return article

    @parse_json
    @retrieve_item(Article, ArticleSchema)
    def patch(self, data, article, **kwargs):
        article = article.update(data)
        return article.save()

    @retrieve_item(Article, ArticleSchema)
    def delete(self, article, **kwargs):
        article.delete()
        return '', 204
