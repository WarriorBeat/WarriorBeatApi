"""
    warriorbeat/api/user/schema.py
    Models for User Profiles & Accounts
"""


from marshmallow import Schema, fields, post_load

from warriorbeat.api.user.model import UserFeedback


class UserFeedbackSchema(Schema):
    """Data Schema for User Feedback"""
    userId = fields.Str(default='GUEST', missing='GUEST')
    feedbackId = fields.Str()
    phone = fields.Str(required=True)
    create_date = fields.Str()
    subject = fields.Str()
    content = fields.Str()

    @post_load
    def make_feedback(self, data):
        """return UserFeedback instance"""
        user_feedback = UserFeedback(**data)
        user_feedback.schema = UserFeedbackSchema()
        return user_feedback
