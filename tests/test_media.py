"""
    Tests for Media Resource
"""

import unittest
import requests
import json
from helper import TestPrint
from test_setup import ApiTestCase


class MediaTest(ApiTestCase):
    base_url = "http://127.0.0.1:5000/api/media"

    def test_create_cover(self):
        """Create Cover Image Test"""
        p = TestPrint('test_create_cover')
        p.info('Test: Create Cover Image')
        mock_request = {
            'mediaId': '1',
            'source': 'www.image.com',
            'credits': '@123ABC Comp.',
            'caption': 'Super Cool Image',
            'title': 'Super Cool Pic'
        }
        mock_data = json.dumps(mock_request)
        p.data('Mock Data', mock_data)
        req = requests.post(self.base_url, json=mock_data)
        reply = req.json()
        ser_reply = json.loads(reply)
        p.data('Serialized Reply', ser_reply)
        expected = dict({'type': 'cover-image'}, **mock_request)
        p.data('Expected Reply', expected)
        assert expected == ser_reply
