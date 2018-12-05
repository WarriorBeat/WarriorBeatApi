"""
    Tests for Media Resource
"""

import json

import requests

from helper import TestPrint
from sample import make_mock_media, media_url
from test_setup import ApiTestCase


class MediaTest(ApiTestCase):

    def test_create_cover(self):
        """Create Cover Image Test"""
        p = TestPrint('test_create_cover')
        p.info('Test: Create Cover Image')
        mock_request = make_mock_media()
        mock_data = json.dumps(mock_request)
        p.data('Mock Data', mock_data)
        req = requests.post(media_url, json=mock_data)
        # Test Data
        reply = req.json()
        ser_reply = json.loads(reply)
        sent_source = mock_request.pop('source')
        rec_source = ser_reply.pop('source')
        p.data('Serialized Reply', ser_reply)
        expected = dict({'type': 'cover-image'}, **mock_request)
        expected['key'] = 'media/super-cool-pic.jpeg'
        p.data('Expected Reply', expected)
        self.assertEqual(expected, ser_reply)
        # Test Image Source

        def get_img_data(url):
            img_stream = requests.get(url, stream=True)
            img_obj = img_stream.raw
            img_data = img_obj.read()
            return img_data
        sent_img = get_img_data(sent_source)
        rec_img = get_img_data(rec_source)
        self.assertEqual(sent_img, rec_img)

    def test_media_save(self):
        """Test if media saves in database"""
        p = TestPrint('test_media_save')
        p.info('Testing Media Save')
        mock_request = make_mock_media()
        mock_data = json.dumps(mock_request)
        p.data('Mock Data', mock_data)
        req = requests.post(media_url, json=mock_data)
        reply = req.json()
        ser_reply = json.loads(reply)
        expected = mock_request.copy()
        expected['source'] = ser_reply['source']
        expected['key'] = ser_reply['key']
        expected['type'] = ser_reply['type']
        db_key = {
            'mediaId': mock_request['mediaId']
        }
        db_content = self.make_db_test(p, self.media_table, db_key)
        p.data('Expected', expected)
        self.assertDictEqual(expected, db_content)
