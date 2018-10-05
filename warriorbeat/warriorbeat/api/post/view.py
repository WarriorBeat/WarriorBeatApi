"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource, request

from warriorbeat.api.post.model import Article
from warriorbeat.api.post.schema import ArticleSchema


class PostList(Resource):

    def get(self):
        return Article.all()

    def post(self):
        article = ArticleSchema().loads(request.json).data
        author = article.author
        cover_image = article.cover_image
        # TODO: Append probably not the best method (MAKE AN UPDATE METHOD)
        author.posts.append(article)
        author.save()
        cover_image.save()
        article.save()
        data = ArticleSchema().dumps(article)
        return data
