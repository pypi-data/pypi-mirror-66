#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

long_description = """
This package is just a placeholder.

You might be looking for https://pypi.org/project/py-solc-x/
"""

setup(
    name="solc",
    version="0.0.0-alpha0",
    description="""placeholder""",
    long_description=long_description,
    author="Ben Hauser",
    author_email="ben@hauser.id",
    py_modules=["solc"],
    setup_requires=[],
    python_requires=">=3.4, <4",
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords="",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
