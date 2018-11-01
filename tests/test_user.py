"""
    Tests for User Resource
"""

import json

import requests

from sample import make_mock_feedback, user_url
from test_setup import ApiTestCase


class UserTest(ApiTestCase):
    def test_create_guest_feedback(self):
        """Create Guest User Feedback Test"""
        mock_feedback = make_mock_feedback(guest=True)
        _req = requests.post(user_url + '/feedback',
                             json=json.dumps(mock_feedback))
        req = json.loads(_req.json())
        del req['create_date']
        del req['feedbackId']
        mock_feedback['userId'] = 'GUEST'
        self.assertDictEqual(req, mock_feedback)
