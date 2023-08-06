#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


info = sys.version_info

setup(
    name='util2',
    version='0.0.0.4',
    install_requires=[],
    description='This is utils library for Python.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nishizumi',
    author_email='daiman003@yahoo.co.jp',
    url='https://github.com/tanaka0079/libs/python/util2/',
    packages=[
        'util2',
        'util2.datetime_extender',
        'util2.file'
    ],  # 提供パッケージ一覧。サブモジュールも忘れずに
    include_package_data=True,
    keywords='util',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['elec=util2.util2:main'],
    },
    test_suite="util2-test",
)
