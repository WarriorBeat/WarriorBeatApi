"""
    warriorbeat/api/author/model.py
    Model for Author Resource
"""
from warriorbeat.utils.data import DynamoDB


class Author(object):
    """Model for Author Resource"""
    db = DynamoDB('author')

    def __init__(self, authorId, name, avatar, posts, title, description):
        self.authorId = authorId
        self.name = name
        self.avatar = avatar
        self.posts = posts
        self.title = title
        self.description = description
        self.schema = None

    @classmethod
    def create_or_retrieve(cls, **kwargs):
        """return an author if it exists, otherwise create one"""
        authorId = kwargs.get('authorId')
        author = cls.db.exists(authorId)
        if not author:
            return cls(**kwargs)
        return cls(**author)

    def save(self):
        dumped = self.schema.dump(self).data
        self.db.add_item(dumped)

    @classmethod
    def all(cls):
        """return all authors"""
        data = cls.db.all
        return data

    def __repr__(self):
        return f'<Author(authorId={self.authorId}, name={self.name})>'

    def __str__(self):
        return f"{self.name}, {self.title}"
