"""
Setup voor de auth status API
"""
from setuptools import setup

setup(
    name='auth-status-api',
    version='0.0.1',
    description='Authentication status reflection REST API',
    packages=['authstatus'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
