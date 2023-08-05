#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from setuptools import setup, find_packages

from wotpy.__version__ import __version__
from wotpy.support import is_dnssd_supported, is_coap_supported, is_mqtt_supported

install_requires = [
    'tornado>=5.1,<6.0',
    'jsonschema>=2.0,<3.0',
    'six>=1.10.0,<2.0',
    'rx>=1.6.0,<2.0',
    'python-slugify>=1.2.4,<2.0'
]

test_requires = [
    'pytest>=3.6.1,<4.0.0',
    'pytest-cov>=2.5.1,<2.6.0',
    'pytest-rerunfailures>=4.1,<5.0',
    'mock>=2.0,<3.0',
    'tox>=2.0,<3.0',
    'faker>=0.8.15,<0.9',
    'Sphinx>=1.7.5,<2.0.0',
    'sphinx-rtd-theme>=0.4.0,<0.5.0',
    'futures>=3.1.1,<4.0.0',
    'pyOpenSSL>=18.0.0,<19.0.0',
    'python-coveralls==2.9.1',
    'coverage==4.0.3'
]

if is_coap_supported():
    install_requires.append('aiocoap[linkheader]==0.4a1')

if is_mqtt_supported():
    install_requires.append('hbmqtt>=0.9.4,<1.0')

if is_dnssd_supported():
    install_requires.append('zeroconf>=0.21.3,<0.22.0')
    test_requires.append('aiozeroconf==0.1.8')

this_dir = path.abspath(path.dirname(__file__))

with open(path.join(this_dir, 'README.md')) as fh:
    long_description = fh.read()

setup(
    name='wotpy',
    version=__version__,
    description='Python implementation of a W3C WoT Runtime and the WoT Scripting API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='wot iot gateway fog w3c',
    author='Andres Garcia Mangas',
    author_email='andres.garcia@fundacionctic.org',
    url='https://github.com/agmangas/wot-py',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
        'uvloop': ['uvloop>=0.12.2,<0.13.0']
    }
)
