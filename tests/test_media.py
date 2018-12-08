"""
    Tests for Media Resource
"""

import json

import requests

from helper import TestPrint
from sample import make_mock_media, media_url
from test_setup import ApiTestCase


def get_img_data(url):
    img_stream = requests.get(url, stream=True)
    img_obj = img_stream.raw
    img_data = img_obj.read()
    return img_data


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
        sent_source = mock_request['source']
        rec_source = ser_reply['url']
        p.data('Serialized Reply', ser_reply)
        expected = dict({'type': 'cover-image'}, **mock_request)
        expected['key'] = 'media/super-cool-pic.jpeg'
        expected['url'] = ser_reply['url']
        p.data('Expected Reply', expected)
        self.assertEqual(expected, ser_reply)
        # Test Image Source
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
        expected['url'] = ser_reply['url']
        expected['key'] = ser_reply['key']
        expected['type'] = ser_reply['type']
        db_key = {
            'mediaId': mock_request['mediaId']
        }
        db_content = self.make_db_test(p, self.media_table, db_key)
        p.data('Expected', expected)
        self.assertDictEqual(expected, db_content)

    def test_media_edit(self):
        """Test Media Edit via Patch"""
        # Create Test Media
        mock_media = make_mock_media()
        _req = requests.post(media_url, json=json.dumps(mock_media))
        media_req = json.loads(_req.json())
        # Mock Patch Request
        mock_url = f"{media_url}/{mock_media['mediaId']}"
        mock_request = {
            'caption': 'Really Cool Image',
            'source': 'https://bit.ly/2N5be49'
        }
        # Expect new caption/source & media attributes
        expected = mock_media
        expected['caption'] = "Really Cool Image"
        expected['key'] = media_req['key']
        expected['source'] = "https://bit.ly/2N5be49"
        expected['type'] = media_req['type']
        # Send Patch Request
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        expected['url'] = req['url']
        # Test new image source
        sent_img = get_img_data("https://bit.ly/2N5be49")
        rec_img = get_img_data(req['url'])
        self.assertEqual(sent_img, rec_img)
        # Assert Data Changes
        self.assertEqual(expected, req)

    def test_media_delete(self):
        """Test Media Deletion"""
        # Create Test Media
        mock_media = make_mock_media()
        _req = requests.post(media_url, json=json.dumps(mock_media))
        # Make Delete Request
        mock_url = f"{media_url}/{mock_media['mediaId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)

    def test_media_overwrite(self):
        """Test Media Overwrite via Put"""
        # Create Test Media
        mock_media = make_mock_media()
        _req = requests.post(media_url, json=json.dumps(mock_media))
        orig_req = _req.json()
        # Overwrite with the following:
        overwrite_mock = make_mock_media(
            title='Best Pic')
        _req = requests.put(f"{media_url}/1", json=json.dumps(overwrite_mock))
        req = json.loads(_req.json())
        # Retrieve Media
        _get_req = requests.get(f"{media_url}/1")
        get_req = _get_req.json()
        # Assert source changed
        orig_source = get_img_data(mock_media['source'])
        rec_source = get_img_data('https://bit.ly/2N5be49')
        self.assertNotEqual(orig_source, rec_source,
                            msg="Media Source did not update")
        # Assert Matching
        self.assertNotEqual(get_req, orig_req)
        self.assertDictEqual(get_req, req)
