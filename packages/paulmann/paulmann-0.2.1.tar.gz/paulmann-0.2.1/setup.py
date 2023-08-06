# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re
import sys
import os

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("paulmann", "__version__.py")
    return re.search(regex, read(*path)).group("version")

def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()

setup(
    name="paulmann",
    version=get_version(),
    description="lib for accessing Paulmann Lichts BLE enabled lights",
    long_description_content_type="text/markdown",
    license="MIT",
    author="mjekovec2",
    author_email="matija@jekovec.net",
    url="https://github.com/mjekovec2/paulmann-lights",
    download_url = "https://github.com/mjekovec2/paulmann-lights/archive/v0.1-alpha.tar.gz", 
    keywords = ['iot', 'bluetooth', 'ble'], 
    packages=find_packages(),
    test_suite="tests",
    install_requires=[
        "attrs>=19.3.0",
        "pygatt>=4.0.5",
        "pexpect>=4.8.0",
        "attr>=0.3.1"
    ],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
