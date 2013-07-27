#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'capimage',
    version = '0.1',
    install_requires = ['sqlalchemy'],
    scripts=['capimage.py']
    )