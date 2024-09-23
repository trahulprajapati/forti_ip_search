"""
MIT License

Project: FortiIPSearch
File: setup.py
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

from setuptools import setup, find_packages

setup(
    name="Fortinet IP Search",
    version="1.01.001",
    url="https://github.com/trahulprajapati/forti_ip_search.git",
    license="MIT",
    author="Rahul Prajapati",
    author_email="trahulprajapati@gmail.com",
    description="Find IP subnet and service provider.",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "amqp==5.2.0",
        "aniso8601==9.0.1",
        "async-timeout==4.0.3",
        "billiard==4.2.1",
        "blinker==1.8.2",
        "cachelib==0.9.0",
        "celery==5.4.0",
        "click==8.1.7",
        "click-didyoumean==0.3.1",
        "click-plugins==1.1.1",
        "click-repl==0.3.0",
        "Flask==3.0.3",
        "Flask-Caching==2.3.0",
        "Flask-Injector==0.15.0",
        "Flask-RESTful==0.3.10",
        "importlib_metadata==8.5.0",
        "injector==0.22.0",
        "Jinja2==3.1.4",
        "joblib==1.4.2",
        "kombu==5.4.2",
        "mypy-extensions==1.0.0",
        "packaging==24.1",
        "pathspec==0.12.1",
        "platformdirs==4.3.6",
        "prompt_toolkit==3.0.47",
        "pytz==2024.2",
        "redis==5.0.8",
        "six==1.16.0",
        "tomli==2.0.1",
        "typing_extensions==4.12.2",
        "tzdata==2024.1",
        "vine==5.1.0",
        "wcwidth==0.2.13",
        "Werkzeug==3.0.4",
        "zipp==3.20.2",
        "uwsgi==2.0.26",
    ],
)
