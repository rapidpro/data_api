#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os.path
import re
from codecs import open

from setuptools import setup

ROOT = os.path.realpath(os.path.dirname(__file__))
init = os.path.join(ROOT, 'data_api', '__init__.py')
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))


def get_requirements(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=NAME,
    version=VERSION,
    author='UNICEF',
    author_email='rapidpro@unicef.org',
    url='',
    description='',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    packages=('data_api', ),
    zip_safe=False,
    license='BSD',
    include_package_data=True,
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        'Framework :: Django',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
    ],
)