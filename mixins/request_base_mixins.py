"""
MIT License

Project: FortiIPSearch
File: request_base_mixins.py
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

from typing import List

# from flask import current_app, json,


class BaseSerielizerMixins:
    _MANDATE_FIELDS = []

    def __init__(self):
        self._is_valid = False
        self._errors = []

    def _validate_mandate_fields(self, request) -> bool:
        if self._MANDATE_FIELDS:
            input_data = request.get_json()
            for field in self._MANDATE_FIELDS:
                if not input_data.get(field):
                    self._errors.append(f"{field} is mandatory")
                    return False
        return True

    def validate(self, request, *args, **kwargs):
        self._is_valid = self._validate_mandate_fields(request)

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def errors(self) -> List[str]:
        return self._errors

    def validate_status(self, status: bool, error=None):
        is_valid = self.is_valid and status
        if not is_valid:
            self._errors.append(error)
        self._is_valid = is_valid
