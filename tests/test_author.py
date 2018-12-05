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
        """Author Creation Test"""
        p = TestPrint('test_create')
        p.info("Testing Author Creation")
        mock_request = make_mock_author()
        mock_data = json.dumps(mock_request)
        p.data('Mock Request', mock_request)
        _req = requests.post(author_url, json=mock_data)
        req = json.loads(_req.json())
        mock_request['profile_image'] = req['profile_image']
        # Title should be parsed from ['administrator', 'staff_writer'] => "Staff Writer"
        mock_request['title'] = "Staff Writer"
        # Author should be returned with empty array for posts attribute
        mock_request['posts'] = []
        p.data('Expected', mock_request)
        self.assertDictEqual(mock_request, req)

    def test_author_saved(self):
        """Author DB Save Test"""
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
            db_item = _resp['Item']
        except KeyError:
            t.info('FAILED')
            scan = self.author_table.scan()
            items = scan["Items"]
            t.data('DATABASE DUMP', items)
            self.fail(f'Author Not Saved to database: {items}')
        mock_request['profile_image'] = db_item['profile_image']
        mock_request['title'] = "Staff Writer"
        mock_request['posts'] = []
        t.data('Expected', mock_request)
        self.assertDictEqual(mock_request, db_item)


if __name__ == '__main__':
    unittest.main()
