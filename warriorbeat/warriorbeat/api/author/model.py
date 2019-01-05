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
    relations = ['profile_image', 'posts']

    def __init__(self, authorId, **kwargs):
        self.authorId = authorId
        self.name = kwargs.get('name')
        self.profile_image = kwargs.get('profile_image')
        self.posts = kwargs.get('posts', [])
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.post_count = str(len(self.posts))
        self.staff_year = kwargs.get('staff_year')
        self.grade_year = kwargs.get('grade_year')

    def add_post(self, postId, *args, **kwargs):
        """adds postId to author posts"""
        if postId not in self.posts:
            self.posts.append(postId)
            self.post_count = str(len(self.posts))
            self = super().update(
                {'posts': self.posts, 'post_count': self.post_count})
            return self.save()
        return self

    def __repr__(self):
        return f'<Author(authorId={self.authorId}, name={self.name})>'

    def __str__(self):
        return f"{self.name}, {self.title}"
