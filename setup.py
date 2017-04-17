#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom plugin for Resolwe SDK for Python used at BCM

See: https://github.com/linlabcode/resolwe-bio-py-bcm

The MIT License (MIT)
Copyright (c) 2017 Charles Y. Lin, Domen Blenkuš, Barbara Jenko, Rachel Hirsch
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from setuptools import setup, find_packages
from codecs import open  # Use codecs' open for a consistent encoding
from os import path


base_dir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get package metadata from 'resolwe.__about__.py' file
about = {}
with open(path.join(base_dir, 'resdk_bcm', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],

    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,

    url=about['__url__'],

    author=about['__author__'],
    author_email=about['__email__'],

    license=about['__license__'],

    packages=find_packages(exclude=['tests', 'tests.*', '*.tests', '*.tests.*']),

    zip_safe=False,
    install_requires=(
        'pexpect>=4.2.1',
        'six>=1.10.0',
        'resdk>=1.7.0',
    ),
    extras_require={
        'package': [
            'twine',
            'wheel',
        ],
        'test': [
            'check-manifest',
            'pycodestyle>=2.1.0',
            'pydocstyle>=1.0.0',
            'pylint~=1.7.0',
            'readme_renderer',
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='bioinformatics resolwe bio pipelines dataflow django python sdk',
)
