
from setuptools import Command, find_packages, setup
import falcon_params_verifier

import io
import os
import sys

# Package meta-data.
NAME = 'falcon_params_verifier'
DESCRIPTION = 'A simple Falcon API "hook" to verify if a provided list of query parameters have been fulfilled.'
URL = 'https://github.com/ms7m/falcon-params-verifer'
EMAIL = 'ms7mohamed@gmail.com'
AUTHOR = 'Mustafa Mohamed'
REQUIRES_PYTHON = '>=3.6.0'


here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=falcon_params_verifier.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)