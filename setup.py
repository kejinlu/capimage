#!/usr/bin/env python
from distutils.core import setup
import os
import shutil

if not os.path.exists('scripts'):
    os.makedirs('scripts')
shutil.copyfile('capimage.py', 'scripts/capimage')

setup(
    name = 'capimage',
    version = '0.1',
    scripts=['capimage.py']
    )