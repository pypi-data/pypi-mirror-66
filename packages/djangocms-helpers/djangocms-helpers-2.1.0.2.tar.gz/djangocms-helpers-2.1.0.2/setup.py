#!/usr/bin/env python3
from setuptools import setup


setup(
    name='djangocms-helpers',
    version='2.1.0.2',
    author='Victor',
    author_email='victor@what.digital',
    url='https://gitlab.com/what-digital/djangocms-helpers',
    packages=[
        'djangocms_helpers',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.2, < 3',
        'django-fieldsignals >= 0.4.0',
        'django-meta',
    ],
)
