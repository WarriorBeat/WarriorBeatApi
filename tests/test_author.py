"""
    Tests for Author Resource
"""

import json
import unittest

import requests

from helper import TestPrint
from sample import author_url, make_mock_author
from test_setup import ApiTestCase


class AuthorTest(ApiTestCase):

    def test_create_author(self):
        p = TestPrint('test_create')
        p.info("Testing Author Creation")
        self.mock_request = make_mock_author()
        mock_data = json.dumps(self.mock_request)
        p.data('Mock Request', self.mock_request)
        req = requests.post(author_url, json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        self.mock_request['profile_image'] = ser_reply['profile_image']
        p.data('Expected', self.mock_request)
        self.assertDictEqual(self.mock_request, ser_reply)

    def test_author_saved(self):
        mock_request = make_mock_author(id='2')
        requests.post(author_url, json=json.dumps(mock_request))
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
        mock_request['profile_image'] = resp['profile_image']
        t.data('Expected', mock_request)
        self.assertDictEqual(mock_request, resp)


if __name__ == '__main__':
    unittest.main()
