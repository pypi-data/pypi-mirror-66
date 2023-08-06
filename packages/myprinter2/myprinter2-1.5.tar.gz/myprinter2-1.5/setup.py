#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="myprinter2",
    version='1.5',
    description="Test setuptools",
    url="http://pypi.python.org/pypi/myprinter2/",
    author="fshenx",
    author_email="333@qq.com",
    license="LICENSE",
    packages=find_packages(),
    data_files=[('myprinter2/config', ['myprinter2/config/t.json']),]
)
