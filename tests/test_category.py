"""
    Tests for Category Resource
"""
import json

import requests

from sample import category_url, make_mock_category
from test_setup import ApiTestCase


class CategoryTest(ApiTestCase):

    def test_create_category(self):
        """Test Category Creation"""
        mock_request = make_mock_category()
        _req = requests.post(category_url, json=json.dumps(mock_request))
        req = json.loads(_req.json())
        self.assertDictEqual(mock_request, req)

    def test_category_edit(self):
        """Test Category Edit via Patch"""
        # Create Test Category
        mock_category = make_mock_category()
        _req = requests.post(category_url, json=json.dumps(mock_category))
        # Mock Patch Request
        mock_url = f"{category_url}/{mock_category['categoryId']}"
        mock_request = {
            'name': 'Sports'
        }
        # Expect same but with name from News ==> Sports
        expected = mock_category
        expected['name'] = 'Sports'
        # Send Patch Request
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        self.assertDictEqual(expected, req)

    def test_category_delete(self):
        """Test Category Deletion"""
        # Create Test Category
        mock_category = make_mock_category()
        _req = requests.post(category_url, json=json.dumps(mock_category))
        # Make Delete Request
        mock_url = f"{category_url}/{mock_category['categoryId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)
