"""
    warriorbeat/api/poll/view.py
    View for Poll Resource
"""


from flask_restful import Resource

from warriorbeat.api.poll.model import Poll
from warriorbeat.api.poll.schema import PollSchema
from warriorbeat.utils import parse_json, retrieve_item, use_schema


class PollList(Resource):

    def get(self):
        return Poll.all()

    @use_schema(PollSchema(), dump=True)
    def post(self, poll):
        poll.save()
        return poll


class PollItem(Resource):

    @retrieve_item(Poll)
    def get(self, poll, **kwargs):
        return poll

    @parse_json
    @retrieve_item(Poll, PollSchema)
    def patch(self, data, poll, **kwargs):
        poll = poll.update(data)
        return poll.save()

    @use_schema(PollSchema(), dump=True)
    def put(self, poll, pollId):
        poll.save()
        return poll

    @retrieve_item(Poll, PollSchema)
    def delete(self, poll, **kwargs):
        poll.delete()
        return '', 204
