"""
    Tests for User Resource
"""

import json

import requests

from sample import make_mock_feedback, user_url
from test_setup import ApiTestCase

feedback_url = user_url + '/feedback'


class UserTest(ApiTestCase):
    def test_create_guest_feedback(self):
        """Create Guest User Feedback Test"""
        mock_feedback = make_mock_feedback(guest=True)
        _req = requests.post(feedback_url,
                             json=json.dumps(mock_feedback))
        req = json.loads(_req.json())
        mock_feedback['feedbackId'] = req['feedbackId']
        mock_feedback['userId'] = 'GUEST'
        self.assertDictEqual(req, mock_feedback)

    def test_feedback_edit(self):
        """Test Feedback Edit via Patch"""
        # Create Test Feedback
        mock_feedback = make_mock_feedback(guest=True)
        _req = requests.post(feedback_url, json=json.dumps(mock_feedback))
        feedback_req = json.loads(_req.json())
        # Mock Patch Request
        mock_url = f"{feedback_url}/{feedback_req['feedbackId']}"
        mock_request = {
            'content': 'Awesome!'
        }
        # Expect same but with content changed & feedback attrs
        expected = mock_feedback
        expected['content'] = 'Awesome!'
        expected['feedbackId'] = feedback_req['feedbackId']
        expected['create_date'] = feedback_req['create_date']
        expected['userId'] = 'GUEST'
        # Send Patch Request
        _req = requests.patch(mock_url, json=json.dumps(mock_request))
        req = _req.json()
        self.assertDictEqual(expected, req)

    def test_feedback_delete(self):
        """Test Feedback Deletion"""
        # Create Test Feedback
        mock_feedback = make_mock_feedback(guest=True)
        _req = requests.post(feedback_url, json=json.dumps(mock_feedback))
        feedback_req = json.loads(_req.json())
        # Make Delete Request
        mock_url = f"{feedback_url}/{feedback_req['feedbackId']}"
        req = requests.delete(mock_url)
        self.assertEqual(req.status_code, 204)
        get_req = requests.get(mock_url)
        self.assertEqual(get_req.status_code, 404)
