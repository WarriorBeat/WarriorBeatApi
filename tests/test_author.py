"""
    Tests for Author Resource
"""

import unittest
import requests
import json
from helper import TestPrint
from test_setup import ApiTestCase


class AuthorTest(ApiTestCase):

    def test_create_author(self):
        p = TestPrint('test_create')
        p.info("Testing Author Creation")
        self.mock_request = {
            'authorId': '2',
            'name': 'Test Author',
            'avatar': 'https://bit.ly/2QmP0eM',
            'posts': [],
            'title': 'Staff Writer',
            'description': 'Hi, I am a test author!'
        }
        mock_data = json.dumps(self.mock_request)
        p.data('Mock Json', mock_data)
        req = requests.post(
            'http://127.0.0.1:5000/api/authors', json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        self.assertDictEqual(self.mock_request, ser_reply)

    def test_author_saved(self):
        self.test_create_author()
        t = TestPrint('test_author_saved')
        _resp = self.author_table.get_item(
            Key={
                'authorId': '2'
            }
        )
        t.data('_resp Data', _resp)
        try:
            resp = _resp['Item']
        except KeyError:
            t.info('FAILED')
            scan = self.author_table.scan()
            items = scan["Items"]
            t.data('DATABASE DUMP', items)
        self.assertDictEqual(self.mock_request, resp)


if __name__ == '__main__':
    unittest.main()
