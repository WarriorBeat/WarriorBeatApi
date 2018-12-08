"""
    Tests for Poll Resource
"""
import json

import requests

from sample import make_mock_poll, poll_url
from test_setup import ApiTestCase


class PollTest(ApiTestCase):

    def test_create_poll(self):
        """Test Poll Creation"""
        mock_request = make_mock_poll()
        _req = requests.post(poll_url, json=json.dumps(mock_request))
        req = json.loads(_req.json())
        expected = mock_request
        expected['total_votes'] = '8'
        self.assertDictEqual(req, expected)

    def test_poll_vote(self):
        """Test Poll Vote via Patch"""
        # Create Test Poll
        mock_poll = make_mock_poll()
        _req = requests.post(poll_url, json=json.dumps(mock_poll))
        req = json.loads(_req.json())
        # Setup Fake 'Vote Action' for Poll
        mock_url = f"{poll_url}/{req['pollId']}"
        mock_request = {
            "answers": [
                {
                    "answerId": "0",
                    "votes": "6"  # Increased from default 5
                },
                {
                    "answerId": "1",
                    "votes": "3"
                },
            ]
        }
        expected = req
        expected['answers'][0] = mock_request['answers'][0]
        expected['answers'][0]['answer'] = 'Yes'
        expected['total_votes'] = '9'
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        self.assertDictEqual(req, expected)

    def test_poll_delete(self):
        """Test Poll Deletion"""
        mock_poll = make_mock_poll()
        _req = requests.post(poll_url, json=json.dumps(mock_poll))
        mock_url = f"{poll_url}/{mock_poll['pollId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)
