"""
MIT License

Project: FortiIPSearch
File: wsgi.py
Copyright (c) 2024 Rahul Prajapati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import unittest
import json

from server import app
from common.constants import Constants as const


class SearchIPUnitTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client"""
        self.app = app.test_client()
        self.app.testing = True
        self._api_endpoint = "/search-ip-prefix/v1/search-ip"

    def test_positive_get_ip_details_single_ip(self):
        input_data = {const.IP: "18.154.10.90", const.REQUEST_TYPE: const.SINGLE_IP}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        result = response.get_json()
        expected_data = {
            "data": [
                {
                    "18.154.0.0/15": {
                        "service": "AWS",
                        "subnet": "18.154.0.0/15",
                        "tags": ["Cloud", "CDN"],
                    }
                },
                {
                    "18.154.0.0/15": {
                        "service": "AWS",
                        "subnet": "18.154.0.0/15",
                        "tags": ["Cloud"],
                    }
                },
            ],
            "message": ["Successful"],
            "status": 202,
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_data)

    def test_positive_get_ip_details_single_ip_subnet_not_found(self):
        input_data = {const.IP: "195.21.11.4", const.REQUEST_TYPE: const.SINGLE_IP}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        result = response.get_json()
        expected_data = {"data": [], "message": ["Successful"], "status": 202}

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_data)

    def test_negative_get_ip_details_single_invalid_ip(self):
        input_data = {const.IP: "18.154.100", const.REQUEST_TYPE: const.SINGLE_IP}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        expected_message = (
            "Validation Error: ['18.154.100 IP is not valid', "
            "'single request type if not valid. Valid request types are: ']"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_data(as_text=True), expected_message)

    def test_negative_get_ip_details_single_without_ip(self):
        input_data = {const.REQUEST_TYPE: const.SINGLE_IP}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        expected_message = "Validation Error: ['ip is mandatory']"
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_data(as_text=True), expected_message)

    def test_negative_get_ip_details_single_without_request_type(self):
        input_data = {const.IP: "18.154.100"}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        expected_message = "Validation Error: ['request_type is mandatory']"
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_data(as_text=True), expected_message)

    def test_positive_get_ip_details_batch_ip(self):
        ip_batch = [
            "18.154.10.90",
            "181.154.10.91",
            "138.154.10.92",
            "118.154.10.93",
            "218.154.10.94",
            "18.14.210.96",
            "18.14.10.97",
            "118.154.10.98",
            "108.154.10.89",
            "180.154.110.65",
            "114.154.210.39",
            "104.154.11.90",
            "189.154.11.91",
            "138.154.11.92",
            "158.154.11.93",
            "184.51.33.230",
            "128.154.11.96",
            "198.154.11.97",
            "108.154.11.98",
            "18.154.101.89",
            "185.154.131.65",
            "185.14.121.39",
        ]
        input_data = {const.IP: ip_batch, const.REQUEST_TYPE: const.BATCH_IP}
        response = self.app.post(
            self._api_endpoint,
            data=json.dumps(input_data),
            content_type="application/json",
        )
        result = response.get_json()
        expected_data = {
            "data": {
                "104.154.11.90": [],
                "108.154.10.89": [],
                "108.154.11.98": [],
                "114.154.210.39": [],
                "118.154.10.93": [],
                "118.154.10.98": [],
                "128.154.11.96": [],
                "138.154.10.92": [],
                "138.154.11.92": [],
                "158.154.11.93": [],
                "18.14.10.97": [],
                "18.14.210.96": [],
                "18.154.10.90": [
                    {
                        "18.154.0.0/15": {
                            "service": "AWS",
                            "subnet": "18.154.0.0/15",
                            "tags": ["Cloud", "CDN"],
                        }
                    },
                    {
                        "18.154.0.0/15": {
                            "service": "AWS",
                            "subnet": "18.154.0.0/15",
                            "tags": ["Cloud"],
                        }
                    },
                ],
                "18.154.101.89": [
                    {
                        "18.154.0.0/15": {
                            "service": "AWS",
                            "subnet": "18.154.0.0/15",
                            "tags": ["Cloud", "CDN"],
                        }
                    },
                    {
                        "18.154.0.0/15": {
                            "service": "AWS",
                            "subnet": "18.154.0.0/15",
                            "tags": ["Cloud"],
                        }
                    },
                ],
                "180.154.110.65": [],
                "181.154.10.91": [],
                "184.51.33.230": [
                    {
                        "184.51.33.0/24": {
                            "service": "Akamai",
                            "subnet": "184.51.33.0/24",
                            "tags": ["Cloud", "CDN/WAF"],
                        }
                    }
                ],
                "185.14.121.39": [],
                "185.154.131.65": [],
                "189.154.11.91": [],
                "198.154.11.97": [],
                "218.154.10.94": [],
            },
            "message": "",
            "status": 202,
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(result, expected_data)
