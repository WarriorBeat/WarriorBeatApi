"""
    warriorbeat/api/poll/schema.py
    Schema for Poll Resource
"""

from marshmallow import Schema, fields, post_load

from warriorbeat.api.poll.model import Poll


class PollSchema(Schema):
    """Poll Post Type Schema"""

    pollId = fields.String()
    question = fields.String()
    total_votes = fields.Method(
        'get_total_votes', deserialize='load_total_votes')
    status = fields.String()
    answers = fields.Nested('PollAnswerSchema', many=True)
    date = fields.Str()

    def get_total_votes(self, obj):
        """add up votes on answers to get total_votes"""
        total = sum([int(answer['votes']) for answer in obj.answers])
        return str(total)

    def load_total_votes(self, value):
        return str(value)

    @post_load
    def make_poll(self, data):
        """return poll instance"""
        poll = Poll.create_or_update(**data)
        poll.schema = PollSchema()
        return poll


class PollAnswerSchema(Schema):
    """Schema for Poll Answers"""
    answerId = fields.Str()
    answer = fields.Str()
    votes = fields.Str()
