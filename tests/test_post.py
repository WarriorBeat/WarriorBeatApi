"""
    Tests for Post Resource
"""

import json
import unittest

import requests

from helper import TestPrint
from sample import (author_url, category_url, make_mock_article,
                    make_mock_author, make_mock_category, make_mock_media,
                    make_mock_profile_image, media_url, post_url)
from test_setup import ApiTestCase


class PostTest(ApiTestCase):

    def setup_article(self):
        """Create Article resource requirements"""
        mock_author_profile = make_mock_profile_image()
        mock_cover_image = make_mock_media()
        mock_author = make_mock_author()
        mock_category = make_mock_category()
        requests.post(media_url, json=json.dumps(mock_author_profile))
        requests.post(media_url, json=json.dumps(mock_cover_image))
        requests.post(author_url, json=json.dumps(mock_author))
        requests.post(category_url, json=json.dumps(mock_category))
        return {
            'authorId': mock_author['authorId'],
            'category': [mock_category['categoryId']],
            'cover_img': mock_cover_image['mediaId']
        }

    def test_create_article(self):
        """Create Article Request Test"""
        # Create Article
        article_setup = self.setup_article()
        mock_request = make_mock_article(**article_setup)
        _req = requests.post(post_url, json=json.dumps(mock_request))
        req = json.loads(_req.json())
        self.assertDictEqual(mock_request, req)

    def test_post_update(self):
        """Ensure Post updates Author test"""
        article_setup = self.setup_article()
        mock_request = make_mock_article(**article_setup)
        req = requests.post('http://127.0.0.1:5000/api/posts',
                            json=json.dumps(mock_request))
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
        self.assertDictEqual(mock_request, resp)
        # Check Author Updated
        t = TestPrint('test_post_update (author)')
        _resp = self.author_table.get_item(
            Key={
                'authorId': mock_request['author']
            }
        )
        resp = _resp['Item']
        t.data('_resp Data', resp)
        # check if author data contains new postIds
        expected_posts = ['1']
        self.assertEqual(expected_posts, resp['posts'])

    def test_multi_article_save(self):
        """
        Test to ensure author is saving multiple posts
        """
        t = TestPrint('test_multi_article_save')
        article_setup = self.setup_article()
        mock_post_1 = make_mock_article(
            id='5', title='Mock Article #5', **article_setup)
        mock_post_2 = make_mock_article(
            id='6', title='Mock Article #6', **article_setup)
        _resp_1 = requests.post(post_url, json=json.dumps(mock_post_1))
        _resp_2 = requests.post(post_url, json=json.dumps(mock_post_2))
        resp_1 = json.loads(_resp_1.json())
        resp_2 = json.loads(_resp_2.json())
        _resp = self.author_table.get_item(Key={
            'authorId': '1'
        })
        resp = _resp['Item']
        t.data('Received Response', resp)
        expected_posts = [mock_post_1['postId'], mock_post_2['postId']]
        self.assertEqual(expected_posts, resp['posts'])

    def test_create_category(self):
        """Test Category Creation"""
        t = TestPrint('test_create_category')
        mock_request = make_mock_category()
        _req = requests.post(category_url, json=json.dumps(mock_request))
        req = json.loads(_req.json())
        self.assertDictEqual(mock_request, req)

    def test_article_edit(self):
        """Test Article Edit via Patch"""
        # Setup test Article
        article_setup = self.setup_article()
        mock_article = make_mock_article(**article_setup)
        _req = requests.post(post_url, json=json.dumps(mock_article))
        # Create new Cover Image to replace article's current
        mock_cover_img = make_mock_media(id='30', title='Replacement Pic')
        _req = requests.post(media_url, json=json.dumps(mock_cover_img))
        # Mock Patch Request
        mock_url = f"{post_url}/{mock_article['postId']}"
        mock_request = {
            'cover_image': '30'
        }
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        # Expect same article but with new cover_image id
        expected = mock_article
        expected['cover_image'] = '30'
        self.assertDictEqual(expected, req)

    def test_article_delete(self):
        """Test Article Deletion"""
        article_setup = self.setup_article()
        mock_article = make_mock_article(**article_setup)
        _req = requests.post(post_url, json=json.dumps(mock_article))
        mock_url = f"{post_url}/{mock_article['postId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)


if __name__ == '__main__':
    unittest.main()
