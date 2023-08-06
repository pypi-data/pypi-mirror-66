#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

__version__ = "1.0.0"
description = "A library and cli tool for interfacing with Microsoft's Graph API."

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Load requirements
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name='msgapi',

    version=__version__,

    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/ace-ecosystem/msgapi',

    author='Sean McFeely',
    author_email='mcfeelynaes@gmail.com',

    license='Apache-2.0',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
    ],

    keywords='Information Security,Microsoft,GraphAPI,graph api',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    # NOTE: hm, PYTHON_ARGCOMPLETE_OK not working dropping console script like so:
    #entry_points={
    #    'console_scripts': ['msgraphi=msgraphi.cli:main'],
    #}
    # doing this instead:
    scripts=['msgraphi']
)

