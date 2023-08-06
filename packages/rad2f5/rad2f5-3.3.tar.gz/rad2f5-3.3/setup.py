#!/usr/bin/env python
from setuptools import setup, find_packages

import os
import sys
if sys.version_info[0] < 3:
    with open('README.md') as f:
        long_description = f.read()
else:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(
        name="rad2f5",
        version="3.3",
        packages=find_packages(),
        install_requires=['re','ipaddress'],
        long_description=long_description,
        author="Pete White",
        author_email="pwhite@f5.com",
        description="A Python script to convert RadWare configuration to F5 syntax",
        license="PSF",
        url="https://pypi.python.org/pypi?:action=display&name=rad2f5&version=3.3",
)
