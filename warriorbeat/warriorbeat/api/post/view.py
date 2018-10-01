"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource, request

from warriorbeat.api.author.schema import AuthorSchema
from warriorbeat.api.post.schema import ArticleSchema


class PostList(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        article = ArticleSchema().loads(request.json).data
        author = article.author
        # TODO: Append probably not the best method (MAKE AN UPDATE METHOD)
        author.posts.append(article)
        author.save()
        article.save()
        data = ArticleSchema().dumps(article)
        return data
