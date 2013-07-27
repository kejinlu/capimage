#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil

if not os.path.exists('scripts'):
    os.makedirs('scripts')
shutil.copyfile('capimage.py', 'scripts/capimage')

setup(
    name = 'capimage',
    version = '0.1',
    scripts=['scripts/capimage'],
    author = '卢克进',
    author_email = 'kejinlu@gmail.com',
    url = 'https://github.com/kejinlu/capimage',
    description = 'Generate resizable image with cap insets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Graphics',
        ]
    )