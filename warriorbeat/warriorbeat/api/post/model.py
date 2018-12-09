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
    relations = ["author", "categories", "cover_image"]

    def __init__(self, postId, **kwargs):
        self.postId = postId
        self.title = kwargs.get('title')
        self.type = kwargs.get('type')
        self.date = kwargs.get('date')

    def __str__(self):
        return f"({self.type}) {self.title} by {self.author}"


class Article(Post):
    """Model for Article Post Type"""

    def __init__(self, *args, **kwargs):
        self.categories = kwargs.get('categories')
        self.author = kwargs.get('author')
        self.cover_image = kwargs.get('cover_image')
        self.content = kwargs.get('content')
        super(Article, self).__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        """override create to update author"""
        author = self.author
        author.add_post(self.postId)
        return super().save(*args, **kwargs)
