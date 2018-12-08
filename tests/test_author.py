"""
    Tests for Author Resource
"""

import json
import unittest

import requests

from helper import TestPrint
from sample import (author_url, make_mock_author, make_mock_profile_image,
                    media_url)
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

    def test_author_edit(self):
        """Test Author Edit via Patch"""
        # Create test author profile image
        mock_profile = make_mock_profile_image()
        _req = requests.post(media_url, json=json.dumps(mock_profile))
        # Create test author
        mock_author = make_mock_author()
        _req = requests.post(author_url, json=json.dumps(mock_author))
        # Mock Patch Request
        mock_url = f"{author_url}/{mock_author['authorId']}"
        mock_request = {
            'name': "Johnny Appleseed",
            'description': "Yep"
        }
        # Expect same author but with new name/desc
        expected = mock_author
        expected['name'] = "Johnny Appleseed"
        expected['description'] = "Yep"
        expected['posts'] = []
        # Title should be parsed from ['administrator', 'staff_writer'] => "Staff Writer"
        expected['title'] = "Staff Writer"
        # Send Patch Request
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        self.assertDictEqual(expected, req)

    def test_author_delete(self):
        """Test Author Deletion"""
        # Create test author profile image
        mock_profile = make_mock_profile_image()
        _req = requests.post(media_url, json=json.dumps(mock_profile))
        # Create test author
        mock_author = make_mock_author()
        _req = requests.post(author_url, json=json.dumps(mock_author))
        # Make Delete Request
        mock_url = f"{author_url}/{mock_author['authorId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)


if __name__ == '__main__':
    unittest.main()
