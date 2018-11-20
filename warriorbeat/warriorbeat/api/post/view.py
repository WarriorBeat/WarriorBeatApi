"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource

from warriorbeat.api.post.model import Article
from warriorbeat.api.post.schema import ArticleSchema
from warriorbeat.utils import use_schema


class PostList(Resource):

    def get(self):
        return Article.all()

    @use_schema(ArticleSchema(), dump=True)
    def post(self, article):
        author = article.author
        cover_image = article.cover_image
        if article.postId not in author.posts:
            author.posts.append(article.postId)
        author.save()
        cover_image.save()
        article.save()
        return article


class PostItem(Resource):
    def get(self, postId):
        article = Article.retrieve(postId)
        return article
