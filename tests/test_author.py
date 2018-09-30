"""
    Tests for Author Resource
"""

import unittest
import requests
import json
from helper import TestPrint


class AuthorTest(unittest.TestCase):

    def test_create(self):
        p = TestPrint('test_create')
        p.info("Testing Author Creation")
        mock_request = {
            'authorId': '1',
            'name': 'Test Author',
            'avatar': 'https://bit.ly/2QmP0eM',
            'posts': [],
            'title': 'Staff Writer',
            'description': 'Hi, I am a test author!'
        }
        mock_data = json.dumps(mock_request)
        p.data('Mock Json', mock_data)
        req = requests.post(
            'http://127.0.0.1:5000/api/authors', json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        assert mock_request == ser_reply

    def __repr__(self):
        return f"AuthorTest"


if __name__ == '__main__':
    unittest.main()
