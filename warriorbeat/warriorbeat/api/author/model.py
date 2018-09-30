"""
    warriorbeat/api/author/model.py
    Model for Author Resource
"""


class Author(object):
    """Model for Author Resource"""

    def __init__(self, authorId, name, avatar, posts, title, description):
        self.authorId = authorId
        self.name = name
        self.avatar = avatar
        self.posts = posts
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<Author(authorId={self.authorId}, name={self.name})>'
