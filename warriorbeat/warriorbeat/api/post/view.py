"""
    warriorbeat/api/post/view.py
    View for Post Resource
"""


from flask_restful import Resource, request

from warriorbeat.api.post.schema import ArticleSchema


class PostList(Resource):
    def get(self):
        pass

    def post(self):
        data = request.get_json()
        print(data)
        article = ArticleSchema().loads(request.json).data
        print(article.author)
        print(article)
        data = ArticleSchema().dumps(article)
        return data
