"""
    warriorbeat/api/author/model.py
    Model for Author Resource
"""
from warriorbeat.api.model import ResourceModel
from warriorbeat.utils import DynamoDB


class Author(ResourceModel):
    """Model for Author Resource"""
    db = DynamoDB('author')
    identity = 'authorId'

    def __init__(self, authorId, **kwargs):
        self.authorId = authorId
        self.name = kwargs.get('name')
        self.profile_image = kwargs.get('profile_image')
        self.posts = kwargs.get('posts', [])
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')

    def __repr__(self):
        return f'<Author(authorId={self.authorId}, name={self.name})>'

    def __str__(self):
        return f"{self.name}, {self.title}"
