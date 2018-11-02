"""
    warriorbeat/api/post/model.py
    Models for Post Resource
"""

from warriorbeat.api.model import ResourceModel
from warriorbeat.utils import DynamoDB


class Post(ResourceModel):
    """Base Model for Post Resource"""
    db = DynamoDB('post')
    identity = 'postId'

    def __init__(self, postId, **kwargs):
        self.postId = postId
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.type = kwargs.get('type')
        self.categories = kwargs.get('categories')

    def __str__(self):
        return f"({self.type}) {self.title} by {self.author}"


class Article(Post):
    """Model for Article Post Type"""

    def __init__(self, cover_image, content, *args, **kwargs):
        self.cover_image = cover_image
        self.content = content
        super(Article, self).__init__(*args, **kwargs)


class Poll(Post):
    """Model for Poll Post Type"""

    def __init__(self, postId, title, author, type, answers, results):
        super(Poll, self).__init__(postId, title, author, type)
        self.answers = answers
        self.results = results
