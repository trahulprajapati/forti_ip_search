"""
MIT License

Project: FortiIPSearch
File: server.py
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

# Core
import os

# from dotenv import load_dotenv, find_dotenv

# Flask
from flask import Flask, render_template, jsonify, request
from flask_restful import Api
from flask_injector import FlaskInjector, Injector
from injector import singleton, Binder
from celery_app.celery_init import celery_init_app

# App Core
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from common.constants import Constants as const

# Dependency Injection
from api.di.dependency_injector import configure

# Services
from api.services.ip_prefix_source_handler_service import IPPrefixSourceHandlerService
from api.services.redis_service import RedisService

# Views
from api.controllers.seatch_ip_controller import SearchIPPrefixController


# load_dotenv(find_dotenv())


def create_app():
    env = os.environ.get(const.ENVIRONMENT, const.DEVELOPMENT)
    app = Flask(__name__)
    app.config[const.REDIS_URL] = const.DEFAULT_REDIS_URL
    if env == const.PRODUCTION:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    celery_config = {
        const.CELERY: {
            const.BROKER_URL: app.config.get(const.BROKER_URL),
            const.RESULT_BACKEND: app.config.get(const.RESULT_BACKEND),
        }
    }
    app.config.from_mapping(celery_config)
    app.config.from_prefixed_env()
    celery_init_app(app)
    app.config[const.DATA_PATH] = app.root_path + app.config.get(const.DATA_PATH)
    return app


app = create_app()
api = Api(app)

# URL routes
api.add_resource(SearchIPPrefixController, "/search-ip-prefix/v1/search-ip")


def configure(binder: Binder):
    binder.bind(
        IPPrefixSourceHandlerService, to=IPPrefixSourceHandlerService, scope=singleton
    )
    redis_service = RedisService(app.config[const.REDIS_URL])
    binder.bind(RedisService, to=redis_service, scope=singleton)


FlaskInjector(app=app, modules=[configure])


if __name__ == "__main__":
    # TODO Logger implementations
    app.run(port=app.config[const.PORT], debug=True)
