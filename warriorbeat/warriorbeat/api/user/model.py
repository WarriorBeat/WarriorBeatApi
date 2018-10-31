"""
    warriorbeat/api/user/model.py
    Models for User Profiles & Accounts
"""

from warriorbeat.utils.data import DynamoDB


class UserFeedback(object):
    """Model for User Feedback/Suggestions"""
    db = DynamoDB('feedback')

    def __init__(self, *args, **kwargs):
        self.userId = kwargs.get('userId')
        self.phone = kwargs.get('phone')
        self.create_date = kwargs.get('create_date')
        self.subject = kwargs.get('subject')
        self.content = kwargs.get('content')
        self.feedbackId = kwargs.get(
            'feedbackId') or f"{self.phone}_{self.create_date}"
        self.schema = None

    def save(self):
        """save feedback to database"""
        dumped = self.schema.dump(self)
        self.db.add_item(dumped)

    @classmethod
    def all(cls):
        """return all feedbacks"""
        data = cls.db.all
        return data
