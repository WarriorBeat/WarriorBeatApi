"""
    warriorbeat/api/post/model.py
    Models for Post Resource
"""

from warriorbeat.utils.data import DynamoDB


class Post(object):
    """Base Model for Post Resource"""
    db = DynamoDB('post')

    def __init__(self, postId, title, author, type):
        self.postId = postId
        self.title = title
        self.author = author
        self.type = type
        self.schema = None

    def save(self):
        dumped = self.schema.dump(self).data
        self.db.add_item(dumped)

    @classmethod
    def all(cls):
        """return all posts"""
        data = cls.db.all
        return data

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
