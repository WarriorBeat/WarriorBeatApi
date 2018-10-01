"""
    Tests for Post Resource
"""

import unittest
import requests
import json
from helper import TestPrint
from test_setup import ApiTestCase


class PostTest(ApiTestCase):
    def test_create_article(self):
        p = TestPrint('test_create_article')
        p.info('Testing Article Creation')
        mock_author = {
            'authorId': '1',
            'name': 'Test Author'
        }
        mock_request = {
            'postId': '1',
            'title': 'A Test Article',
            'author': mock_author,
            'type': 'article',
            'cover_image': 'https://bit.ly/2QmP0eM',
            'content': 'Filler Content!'
        }
        mock_data = json.dumps(mock_request)
        p.data('Mock Json', mock_data)
        req = requests.post('http://127.0.0.1:5000/api/posts', json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        assert mock_request == ser_reply
