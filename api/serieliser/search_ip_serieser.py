"""
MIT License

Project: FortiIPSearch
File: search_ip_serielizers.py
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

from typing import Dict
from mixins.request_base_mixins import BaseSerielizerMixins
from common.constants import Constants as const
from common.utils import validate_ip


class SearchIPViewSerielizer(BaseSerielizerMixins):
    """
    Serielizers class to validate Search IP controller
    """

    _MANDATE_FIELDS = [const.IP, const.REQUEST_TYPE]

    def validate(self, request, *args, **kwargs) -> Dict[str, str]:
        """
        This is overriding mixins validator, customer validation we can define
        here.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        super().validate(request, *args, **kwargs)
        if not self.is_valid:
            return {}
        input_data = request.get_json()

        # IP validation
        ip = input_data[const.IP]
        is_valid_ip = True
        if isinstance(ip, list):
            for ipa in ip:
                status = validate_ip(ipa)
                if not status:
                    is_valid_ip = False
                    break
        else:
            is_valid_ip = validate_ip(ip)
        error = f"{ip} IP is not valid"
        self.validate_status(is_valid_ip, error)

        # Request type validation
        request_type = input_data[const.REQUEST_TYPE]
        valid_request_ip = [const.BATCH_IP, const.SINGLE_IP]
        is_valid_request_type = request_type in valid_request_ip
        error = f"{request_type} request type if not valid. Valid request types are: "
        self.validate_status(is_valid_request_type, error)
        return {const.IP: ip, const.REQUEST_TYPE: request_type}
