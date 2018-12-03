"""
    Tests for Poll Resource
"""
import json

import requests

from sample import make_mock_poll, poll_url
from test_setup import ApiTestCase


class PostTest(ApiTestCase):

    def test_create_poll(self):
        """Test Poll Creation"""
        mock_request = make_mock_poll()
        expected = mock_request
        _req = requests.post(poll_url, json=json.dumps(mock_request))
        req = json.loads(_req.json())
        self.assertDictEqual(req, expected)
