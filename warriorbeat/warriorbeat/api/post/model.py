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

    def __init__(self, postId, title, author, type):
        self.postId = postId
        self.title = title
        self.author = author
        self.type = type

    def __str__(self):
        return f"({self.type}) {self.title} by {self.author}"


class Article(Post):
    """Model for Article Post Type"""

    def __init__(self, postId, title, author, type, cover_image, content):
        super(Article, self).__init__(postId, title, author, type)
        self.cover_image = cover_image
        self.content = content


class Poll(Post):
    """Model for Poll Post Type"""

    def __init__(self, postId, title, author, type, answers, results):
        super(Poll, self).__init__(postId, title, author, type)
        self.answers = answers
        self.results = results
