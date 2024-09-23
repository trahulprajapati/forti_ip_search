"""
MIT License

Project: FortiIPSearch
File: ip_prefix_source_handler_service.py
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

from typing import List, Union, Dict
import os
import json
import pickle
from http import HTTPStatus
import joblib

from common.constants import Constants as const

from api.services.ip_prefix_source_service import IPPrefixTransformerService


class IPPrefixSearchResponse:
    def __init__(
        self,
        data: Union[List[any], Dict[str, any]],
        status: HTTPStatus,
        message: List[str] = "",
    ):
        self._data = data
        self._status = status
        self._message = message

    @property
    def data(self) -> List[any]:
        return self._data

    @property
    def status(self) -> int:
        return self._status

    @property
    def message(self) -> str:
        return self._message


class IPPrefixSourceHandlerService:
    def __init__(self):
        self._transformed_source_obj = None

    def transform_data(self, source_raw_file: str) -> List[any]:
        """
        Transform input json data to Tries to search ip subnet in effiecient way.
        Instead of transform data on every request, transform once and use this in every request.
        To achive this we will:
        1) Transform the json to trie.
        2) Once transformation is done, dump the Trie object in
            data location i.e static/source_data/transformed_data.joblib
        3) When request comes then use this object.
        4) Search the requested ip in Trie object.

        Parameters
        ----------
        source_raw_file: str
            JSON file.

        Returns
        -------
        None
        """
        with open(source_raw_file, const.READ_FILE_HANDLER) as f:
            raw_data = json.load(f)

        # Creating list of all service items Tries node,
        # At the time of searching will use this list to find the all subnet for requested ip
        transformed_service_obj = []
        for service_name, service in raw_data.items():
            for service_item in service:
                service_transformed_trie = IPPrefixTransformerService()
                subnet_prefix_list = service_item[const.PREFIXES]
                service_tags = service_item[const.TAGS]
                for subnet in subnet_prefix_list:
                    prefix_details = {
                        const.SERVICE: service_name,
                        const.SUBNET: subnet,
                        const.TAGS: service_tags,
                    }
                    service_transformed_trie.insert_subnet(subnet, prefix_details)
                transformed_service_obj.append(service_transformed_trie)
        self._transformed_source_obj = transformed_service_obj
        return transformed_service_obj

    def search_ip_in_subnet(self, ip: str) -> IPPrefixSearchResponse:
        """
        Find all subnet details (services and tags) using this IP.

        Parameters
        ----------
        ip: str
            IP address to find the source.

        Returns
        -------
        matched_subnet: List[any]
            All Matching subnet details.
        """
        matched_subnets = []
        is_request_failed = False
        message = []
        for subnet_obj in self._transformed_source_obj:
            try:
                matched_subnet = subnet_obj.search_ip(ip)
                if matched_subnet:
                    matched_subnets.append(matched_subnet)
            except Exception as err:
                message.append(str(err))
                is_request_failed = True
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if not is_request_failed:
            message = ["Successful"]
            status = HTTPStatus.ACCEPTED
        response = IPPrefixSearchResponse(
            data=matched_subnets, status=status, message=message
        )
        return response

    @property
    def get_transformed_object(self) -> List[any]:
        """
        Get transformed object.
        :return: List[str]
            Transformed object.
        """
        return self._transformed_source_obj

    def export_data(self, object_joblib_file_path: str) -> List[any]:
        """
        Dump the transformed object to joblib file.
        First time this will be saved and after evert iteration of request
        This file(joblib) will be used to set _transformed_source_obj for searching.

        :param object_joblib_file_path: str:
            Transformed Source joblib file.
        :return: List[str]:
            Transformed source object
        """
        joblib.dump(self._transformed_source_obj, object_joblib_file_path)
        return self._transformed_source_obj

    def set_object(self, data_path: str, redis_cache):
        """
        There are two approaches for this:
        1)  Set source transformed file to class.
            This will be used in every request to search IP
        2) Using Caching (Caching is taking lesser time)
            But implementation is available for both.
        :param data_path: str
            Data path contains files.
        :return:
            None
        """
        if redis_cache.get_key("ip_search_transformed_object"):
            byte_stream = redis_cache.get_key("ip_search_transformed_object")
            self._transformed_source_obj = pickle.loads(byte_stream)
            return
        if data_path is None or data_path == "":
            raise ValueError("Transformed file path is missing")
        if not os.path.exists(data_path):
            # Try transform
            os.mkdir(data_path)
        source_file = data_path + const.RAW_SOURCE_FILE_NAME
        if not os.path.exists(source_file) or os.path.getsize(source_file) == 0:
            raise ValueError("Source File does not exist")

        self.transform_data(source_file)
        byte_stream = pickle.dumps(self.get_transformed_object)
        redis_cache.set_key("ip_search_transformed_object", byte_stream)

    def export_source_file_dump_object(self, data_path: str):
        """
        Dump object and restore at every request.
        :param data_path:
        :return:
        """
        source_file = data_path + const.RAW_SOURCE_FILE_NAME
        transformed_file = data_path + const.TRANSFORMED_FILE_NAME
        if (
            not os.path.exists(transformed_file)
            or os.path.getsize(transformed_file) == 0
        ):
            self.transform_data(source_file)
            self.export_data(transformed_file)
        if not os.path.exists(source_file) or os.path.getsize(source_file) == 0:
            raise ValueError("Transformed File does not exist after transformation")

        transform_object = joblib.load(transformed_file)
        self._transformed_source_obj = transform_object
