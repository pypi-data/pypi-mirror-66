#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="myprinter",
    version='1.2',
    description="Test setuptools",
    url="http://pypi.python.org/pypi/myprinter/",
    author="fshenx",
    author_email="22@qq.com",
    license="LICENSE",
    packages=find_packages(),
    data_files=[('testsetup/config3', ['testsetup/config/t.json']),]
    #include_package_data = True,
    #package_data = {'': ['.json'], '': ['.conf']}
)
