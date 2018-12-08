"""
    warriorbeat/api/user/view.py
    User Resources
"""


from flask_restful import Resource

from warriorbeat.api.user.model import UserFeedback
from warriorbeat.api.user.schema import UserFeedbackSchema
from warriorbeat.utils import parse_json, retrieve_item, use_schema


class UserFeedbackList(Resource):

    def get(self):
        return UserFeedback.all()

    @use_schema(UserFeedbackSchema(), dump=True)
    def post(self, feedback):
        feedback.save()
        return feedback


class UserFeedbackItem(Resource):

    @retrieve_item(UserFeedback)
    def get(self, feedback, **kwargs):
        return feedback

    @parse_json
    @retrieve_item(UserFeedback, UserFeedbackSchema)
    def patch(self, data, feedback, **kwargs):
        feedback = feedback.update(data)
        return feedback.save()

    @retrieve_item(UserFeedback, UserFeedbackSchema)
    def delete(self, feedback, **kwargs):
        feedback.delete()
        return '', 204
