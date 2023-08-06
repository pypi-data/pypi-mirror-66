#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 06:28:50 2019

@author: alexandradarmon
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as rq:
    requirements = rq.read()

setuptools.setup(
    name="punctuation_stylometry",
    version="0.0.5",
    author="alexdarmon",
    author_email="alexandra.darmon@hotmail.fr",
    description="This package represents the code used for the publication of the article  https://arxiv.org/abs/1901.00519",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-darmon/punctuation-stylometry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements.split('\n'),
    dependency_links=[
          'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz#egg=en_core_web_sm'
      ]

)
