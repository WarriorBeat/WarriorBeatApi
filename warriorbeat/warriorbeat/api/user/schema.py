"""
    warriorbeat/api/user/schema.py
    Models for User Profiles & Accounts
"""


from marshmallow import Schema, fields, post_load

from warriorbeat.api.user.model import User, UserFeedback


class UserSchema(Schema):
    """Data Schema for Users"""
    userId = fields.Str()
    devices = fields.List(fields.Str())

    @post_load
    def make_user(self, data):
        """return User instance"""
        user = User.create_or_update(**data)
        user.schema = UserSchema()
        return user


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
