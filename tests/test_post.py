"""
    Tests for Post Resource
"""

import json
import unittest

import requests

from helper import TestPrint
from sample import author_url, make_mock_article, make_mock_author, post_url
from test_setup import ApiTestCase


class PostTest(ApiTestCase):

    def test_create_article(self):
        """Create Article Request Test"""
        mock_author = make_mock_author()
        requests.post(author_url, json=json.dumps(mock_author))
        p = TestPrint('test_create_article')
        p.info(__doc__)
        mock_author = {
            'authorId': mock_author['authorId'],
            'name': mock_author['name']
        }
        self.mock_request = make_mock_article(author=mock_author)
        mock_data = json.dumps(self.mock_request)
        p.data('Mock Json', mock_data)
        req = requests.post(post_url, json=mock_data)
        reply = req.json()
        p.data('Json Reply', reply)
        ser_reply = json.loads(reply)
        cover_img = ser_reply['cover_image']
        self.mock_request['cover_image'] = cover_img
        self.assertDictEqual(self.mock_request, ser_reply)

    def test_post_update(self):
        """
        Test for author saving new post
        """
        t = TestPrint('test_post_update (post)')
        # Create Author
        mock_author = make_mock_author(id='2')
        requests.post(author_url, json=json.dumps(mock_author))
        # Create Article
        mock_author = {
            'authorId': mock_author['authorId'],
            'name': mock_author['name']
        }
        mock_request = make_mock_article(id='1', author=mock_author)
        mock_data = json.dumps(mock_request)
        t.data('Mock Json', mock_data)
        req = requests.post('http://127.0.0.1:5000/api/posts', json=mock_data)
        # Check post saved
        _resp = self.post_table.get_item(
            Key={
                'postId': '1'
            }
        )
        try:
            resp = _resp['Item']
        except KeyError:
            t.info('FAILED')
            scan = self.post_table.scan()
            items = scan["Items"]
            t.data('DATABASE DUMP', items)
            self.fail("Post ID not found in database!")
        resp_coverimg = resp['cover_image']
        mock_request['cover_image'] = resp_coverimg
        t.data('Expected: ', mock_request)
        t.data('resp Data', resp)
        self.assertDictEqual(mock_request, resp)
        # Check Author Updated
        t = TestPrint('test_post_update (author)')
        _resp = self.author_table.get_item(
            Key={
                'authorId': mock_author['authorId']
            }
        )
        resp = _resp['Item']
        t.data('_resp Data', resp)
        # check if author data contains new post data
        expected_subset = {
            'posts': [{
                'postId': '1',
                'title': 'A Test Article',
                'type': 'article',
                'cover_image': mock_request['cover_image'],
                'content': 'Filler Content!'
            }],
        }
        self.assertDictContainsSubset(expected_subset, resp)

    def test_multi_article_save(self):
        """
        Test to make sure author is saving multiple posts
        """
        t = TestPrint('test_multi_article_save')
        _mock_author = make_mock_author(id='2', name='Mock Author Two')
        author_resp = requests.post(author_url, json=json.dumps(_mock_author))
        mock_author = {
            'authorId': _mock_author['authorId'],
            'name': _mock_author['name']
        }
        mock_post_1 = make_mock_article(
            id='5', title='Mock Article #5', author=mock_author)
        mock_post_2 = make_mock_article(
            id='6', title='Mock Article #6', author=mock_author)
        _resp_1 = requests.post(post_url, json=json.dumps(mock_post_1))
        _resp_2 = requests.post(post_url, json=json.dumps(mock_post_2))
        resp_1 = json.loads(_resp_1.json())
        resp_2 = json.loads(_resp_2.json())
        t.data('Response Post 1', resp_1)
        t.data('Response Post 2', resp_2)
        _resp = self.author_table.get_item(Key={
            'authorId': '2'
        })
        resp = _resp['Item']
        t.data('Received Response', resp)
        # Delete two way nested author (would cause inheritance issues in schema)
        del mock_post_1['author']
        del mock_post_2['author']
        # Update mocks cover images
        mock_post_1['cover_image'] = resp_1['cover_image']
        mock_post_2['cover_image'] = resp_2['cover_image']
        expected_subset = {
            'posts': [mock_post_1, mock_post_2]
        }
        t.data('Expected subset', expected_subset)
        self.assertDictContainsSubset(expected_subset, resp)


if __name__ == '__main__':
    unittest.main()
