"""
MIT License

Project: FortiIPSearch
File: ip_search_controller.py
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

from typing import List, Dict
from http import HTTPStatus

from flask import Response, current_app, request, jsonify
from flask_restful import Resource
from injector import inject
from common.constants import Constants as const
from celery_app.tasks import process_ip_batch_multi_worker_task

from api.serieliser.search_ip_serieser import SearchIPViewSerielizer
from api.services.ip_prefix_source_handler_service import (
    IPPrefixSourceHandlerService,
    IPPrefixSearchResponse,
)
from api.services.redis_service import RedisService


class SearchIPPrefixController(Resource):
    """
    Controller to search IP or batch of IP's subnet and services.
    """

    @inject
    def __init__(
        self,
        search_ip_handler_service: IPPrefixSourceHandlerService,
        redis_service: RedisService,
    ):
        self.__name__ = __name__
        self._search_ip_handler_service = search_ip_handler_service
        self._ip_search_serielizer = SearchIPViewSerielizer()
        self._redis_service = redis_service
        self._logger = None

    def post(self, **kwargs):
        """
        Find IP subnet controller, It accept two args:
        ip: Union[str, List]
            List of IP of single ip for finding subnet and services.
        request_type: str
            Whether its single ip or multiple ip request.
        :param kwargs:
        :return:
        """
        input_data = self._ip_search_serielizer.validate(request)
        if not self._ip_search_serielizer.is_valid:
            return Response(
                response=f"Validation Error: {self._ip_search_serielizer.errors}",
                status=403,
            )
        self._search_ip_handler_service.set_object(
            current_app.config.get(const.DATA_PATH), self._redis_service
        )
        response = self._handle_request(input_data)
        return jsonify(
            {
                "data": response.data,
                "status": response.status,
                "message": response.message,
            }
        )

    def _handle_request(self, input_data: Dict[str, any]):
        ip = input_data[const.IP]
        request_type = input_data[const.REQUEST_TYPE]
        if request_type == const.SINGLE_IP:
            return self._search_ip_handler_service.search_ip_in_subnet(ip)
        return self._handle_batch_request(ip)

    def _handle_batch_request(self, ip_batch: List[str]):
        batch_size = len(ip_batch)
        single_worker_ip_batch_length = current_app.config.get(
            const.SINGLE_WORKER_IP_BATCH_LENGTH
        )
        if batch_size < single_worker_ip_batch_length:
            return self._process_ip_batch_single_worker(ip_batch)
        return self._process_ip_batch_multi_worker(ip_batch)

    def _process_ip_batch_single_worker(
        self, ip_batch: List[str]
    ) -> IPPrefixSearchResponse:
        batch_data = {}
        is_failed = False

        for ip in ip_batch:
            response = self._search_ip_handler_service.search_ip_in_subnet(ip)
            if response.status != HTTPStatus.ACCEPTED:
                is_failed = True
            batch_data[ip] = response.data
        status = HTTPStatus.ACCEPTED
        if is_failed:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        return IPPrefixSearchResponse(data=batch_data, status=status)

    @staticmethod
    def _process_ip_batch_multi_worker(ip_batch: List[str]) -> List[any]:
        results = process_ip_batch_multi_worker_task.apply_async(ip_batch)
        results = results.get()
        return results
