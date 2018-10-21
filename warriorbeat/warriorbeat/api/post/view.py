"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource, request
from marshmallow.exceptions import ValidationError
from warriorbeat.api.post.model import Article
from warriorbeat.api.post.schema import ArticleSchema


class PostList(Resource):

    def get(self):
        return Article.all()

    def post(self):
        try:
            article = ArticleSchema().load(request.json)
        except Exception:
            article = ArticleSchema().loads(request.json)
        author = article.author
        cover_image = article.cover_image
        # TODO: Append probably not the best method (MAKE AN UPDATE METHOD)
        author.posts.append(article)
        author.save()
        cover_image.save()
        article.save()
        data = ArticleSchema().dumps(article)
        return data
