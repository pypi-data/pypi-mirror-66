#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

dynamic_requires = []

version = 1.0

setuptools.setup(
    name='notti',
    version=1.0,
    author='Robin Cutshaw',
    author_email='robin@internetlabs.com',
    url='http://github.com/RobinCutshaw/python-notti',
    packages=setuptools.find_packages(),
    scripts=[],
    long_description='A Python API for controlling Notti lights manufactured by Witti',
    description='Python API for controlling Notti lights',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
