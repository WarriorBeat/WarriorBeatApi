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
    total_votes = fields.String()
    status = fields.String()
    answers = fields.Nested('PollAnswerSchema', many=True)
    date = fields.Str()

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
