# coding: utf-8
# !/usr/bin/python

"""
Project: datascitools
Sat 18 Apr 12:57:22 2020
"""

from setuptools import setup, find_packages
from  datascitools._version import __version__, __author__, __email__

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'jason.xing.zhang@gmail.com'


setup(
        name='datascitools',
        version=__version__,
        description='Tools for data science',
        license='MIT License',
        install_requires=[
                    'numpy',
                    'pandas',
                    'scipy'
                ],
        author=__author__,
        author_email=__email__,
        packages=find_packages(),
        platforms='any',
)
