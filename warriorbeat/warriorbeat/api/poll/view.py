"""
    warriorbeat/api/poll/view.py
    View for Poll Resource
"""


from flask_restful import Resource, request

from warriorbeat.api.poll.model import Poll
from warriorbeat.api.poll.schema import PollSchema
from warriorbeat.utils import use_schema


class PollList(Resource):

    def get(self):
        return Poll.all()

    @use_schema(PollSchema(), dump=True)
    def post(self, poll):
        poll.save()
        return poll


class PollItem(Resource):
    def get(self, pollId):
        poll = Poll.retrieve(pollId)
        return poll

    def patch(self, pollId):
        poll = Poll.retrieve_instance(pollId, schema=PollSchema)
        poll.answers = request.json.get('answers', poll.answers)
        return poll.save()
