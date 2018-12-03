"""
    warriorbeat/api/poll/model.py
    Models for Poll Resource
"""

from warriorbeat.api.model import ResourceModel
from warriorbeat.utils import DynamoDB


class Poll(ResourceModel):
    """Model for Poll Resource"""
    db = DynamoDB('poll')
    identity = 'pollId'

    def __init__(self, pollId, **kwargs):
        self.pollId = pollId
        self.question = kwargs.get('question')
        self.answers = kwargs.get('answers')
        self.status = kwargs.get('status')
        self.total_votes = kwargs.get('total_votes')
        self.date = kwargs.get('date')
