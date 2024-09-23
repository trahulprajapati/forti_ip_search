"""
MIT License

Project: FortiIPSearch
File: common.py
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

import os

# from dotenv import load_dotenv, find_dotenv
from common.constants import Constants as const

# load_dotenv(find_dotenv())

redis_host = os.getenv(const.REDIS_HOST, "redis")
redis_port = int(os.getenv(const.REDIS_PORT, 6379))


class CommonConfig:
    SINGLE_WORKER_IP_BATCH_LENGTH = 50
    DATA_PATH = "/static/source_data/"
    DEFAULT_RAW_SOURCE_FILE_PATH = DATA_PATH + const.RAW_SOURCE_FILE_NAME
    DEFAULT_TRANSFORMED_SOURCE_FILE_PATH = DATA_PATH + const.TRANSFORMED_FILE_NAME
    broker_url = f"redis://{redis_host}:{redis_port}/0"
    result_backend = f"redis://{redis_host}:{redis_port}/0"
