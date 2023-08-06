#!/usr/bin/env python
"""Sublime API client package."""
import os

from setuptools import find_packages, setup


def read(fname):
    """Read file and return its contents."""
    with open(os.path.join(os.path.dirname(__file__), fname)) as input_file:
        return input_file.read()


INSTALL_REQUIRES = [
]

setup(
    name="sublime-python",
    version="0.0.1",
    description="",
    url="https://sublimesecurity.com/",
    author="Sublime Security",
    author_email="hello@sublimesecurity.com",
    license="MIT",
    download_url="https://github.com/sublime-security",
)
