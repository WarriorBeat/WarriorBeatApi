"""
    warriorbeat/api/author/model.py
    Model for Author Resource
"""
from warriorbeat.utils.data import DynamoDB


class Author(object):
    """Model for Author Resource"""

    def __init__(self, authorId, name, avatar, posts, title, description):
        self.authorId = authorId
        self.name = name
        self.avatar = avatar
        self.posts = posts
        self.title = title
        self.description = description
        self.db = DynamoDB('author')
        self.schema = None

    def save(self):
        dumped = self.schema.dump(self).data
        self.db.add_item(dumped)

    def __repr__(self):
        return f'<Author(authorId={self.authorId}, name={self.name})>'

    def __str__(self):
        return f"{self.name}, {self.title}"
