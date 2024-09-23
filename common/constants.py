"""
MIT License

Project: FortiIPSearch
File: constants.py
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


class Constants:
    IP = "ip"
    REQUEST_TYPE = "request_type"
    BATCH_IP = "batch"
    SINGLE_IP = "single"
    SINGLE_WORKER_IP_BATCH_LENGTH = "SINGLE_WORKER_IP_BATCH_LENGTH"
    PREFIXES = "prefixes"
    TAGS = "tags"
    READ_FILE_HANDLER = "r"
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    DEBUG = "debug"
    ENVIRONMENT = "env"
    TRANSFORMED_FILE_NAME = "transformed_prefixes.joblib"
    RAW_SOURCE_FILE_NAME = "prefixes.json"
    DATA_PATH = "DATA_PATH"
    DEFAULT_RAW_SOURCE_FILE_PATH = "DEFAULT_RAW_SOURCE_FILE_PATH"
    DEFAULT_TRANSFORMED_SOURCE_FILE_PATH = "DEFAULT_TRANSFORMED_SOURCE_FILE_PATH"
    SERVICE = "service"
    SUBNET = "subnet"
    REDIS_URL = "REDIS_URL"
    DEFAULT_REDIS_URL = "redis://redis:6379/0"
    RESULT_BACKEND = "result_backend"
    BROKER_URL = "broker_url"
    CELERY = "CELERY"
    CELERY_EXTENSION = "celery"
    PORT = "PORT"
    REDIS_HOST = "REDIS_HOST"
    REDIS_PORT = "REDIS_PORT"
