"""
    warriorbeat/api/user/model.py
    Models for User Profiles & Accounts
"""

from warriorbeat.api.model import ResourceModel
from warriorbeat.utils.data import DynamoDB


class User(ResourceModel):
    """Model for User Resource"""
    db = DynamoDB('user')
    identity = 'userId'

    def __init__(self, *args, **kwargs):
        self.userId = kwargs.get('userId')
        self.cognitoId = kwargs.get('cognitoId')
        self.subscriptions = kwargs.get('subscriptions')
        self.liked_posts = kwargs.get('liked_posts')


class UserFeedback(ResourceModel):
    """Model for User Feedback/Suggestions"""
    db = DynamoDB('feedback')
    identity = 'feedbackId'

    def __init__(self, *args, **kwargs):
        self.userId = kwargs.get('userId')
        self.phone = kwargs.get('phone')
        self.create_date = kwargs.get('create_date')
        self.subject = kwargs.get('subject')
        self.content = kwargs.get('content')
        self.feedbackId = kwargs.get(
            'feedbackId') or f"{self.phone}_{self.create_date}"
