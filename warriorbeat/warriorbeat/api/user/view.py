"""
    warriorbeat/api/user/view.py
    User Resources
"""


from flask_restful import Resource

from warriorbeat.api.user.model import UserFeedback
from warriorbeat.api.user.schema import UserFeedbackSchema
from warriorbeat.utils.decorators import use_schema


class UserFeedbackList(Resource):

    def get(self):
        return UserFeedback.all()

    @use_schema(UserFeedbackSchema(), dump=True)
    def post(self, feedback):
        feedback.save()
        return feedback
