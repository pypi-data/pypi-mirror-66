#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import os

top, _ = os.path.split(__file__)
with open(os.path.join(top, 'README.md'), 'r') as fin:
   _long_description = fin.read()
with open(os.path.join(top, 'VERSION'), 'r') as fin:
    version = fin.read().strip() + '+local'
version = '1.1.1'.format(version=version)

setup(
    name='typedobject',
    version=version,

    description='Define real, inheritable, and efficient Python classes using variable annotations',
    long_description=_long_description,
    long_description_content_type='text/markdown',

    author='Martin Vejnár',
    author_email='vejnar.martin@gmail.com',
    url='https://github.com/avakar/typedobject',
    license='0BSD',

    package_dir = {'': 'src'},
    packages=['typedobject'],

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
        ]
    )
