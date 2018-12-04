"""
    warriorbeat/api/poll/view.py
    View for Poll Resource
"""


from flask_restful import Resource

from warriorbeat.api.poll.model import Poll
from warriorbeat.api.poll.schema import PollSchema
from warriorbeat.utils import parse_json, use_schema


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
        if poll is None:
            return '', 404
        return poll

    @parse_json
    def patch(self, data, pollId):
        poll = Poll.update_item(pollId, data, PollSchema)
        return poll.save()

    @use_schema(PollSchema(), dump=True)
    def put(self, poll, pollId):
        poll.save()
        return poll

    def delete(self, pollId):
        poll = Poll.retrieve(pollId, instance=True)
        if poll is None:
            return '', 404
        poll.delete()
        return '', 204
