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
        self.devices = kwargs.get('devices', [])

    def save(self, *args, **kwargs):
        """override save to ensure devices are unique"""
        self.devices.append(self.userId)
        self.devices = set(self.devices)
        return super().save(*args, **kwargs)


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
