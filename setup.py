#!/usr/bin/env python

"""
CEE logging module formatter.
"""
from setuptools import setup


setup(
    name='cee-formatter',
    version='0.1',
    url='https://github.com/urbaniak/cee-formatter',
    license='BSD',
    author='Krzysztof Urbaniak',
    author_email='urban@fail.pl',
    description='CEE logging module formatter.',
    long_description=__doc__,
    py_modules=['cee_formatter'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
