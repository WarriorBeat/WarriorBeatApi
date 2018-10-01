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
        self.upload_sample_author()
        p = TestPrint('test_create_article')
        p.info('Testing Article Creation')
        mock_author = {
            'authorId': '1',
            'name': 'Test Author'
        }
        self.mock_request = {
            'postId': '1',
            'title': 'A Test Article',
            'author': mock_author,
            'type': 'article',
            'cover_image': 'https://bit.ly/2QmP0eM',
            'content': 'Filler Content!'
        }
        mock_data = json.dumps(self.mock_request)
        p.data('Mock Json', mock_data)
        req = requests.post('http://127.0.0.1:5000/api/posts', json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        assert self.mock_request == ser_reply

    def test_post_update(self):
        # Check post saved
        self.test_create_article()
        t = TestPrint('test_post_update (post)')
        _resp = self.post_table.get_item(
            Key={
                'postId': '1'
            }
        )
        t.data('_resp Data', _resp)
        try:
            resp = _resp['Item']
        except KeyError:
            t.info('FAILED')
            scan = self.post_table.scan()
            items = scan["Items"]
            t.data('DATABASE DUMP', items)
        assert self.mock_request == resp
        # Check Author Updated
        t = TestPrint('test_post_update (author)')
        _resp = self.author_table.get_item(
            Key={
                'authorId': '1'
            }
        )
        resp = _resp['Item']
        t.data('_resp Data', resp)
        # remove author (inheritance)
        expected = {
            'authorId': '1',
            'name': 'Test Author',
            'avatar': 'url',
            'posts': [{
                'postId': '1',
                'title': 'A Test Article',
                'type': 'article',
                'cover_image': 'https://bit.ly/2QmP0eM',
                'content': 'Filler Content!'
            }],
            'title': 'Staff Writer',
            'description': 'A Test Sample'
        }
        assert expected == resp
