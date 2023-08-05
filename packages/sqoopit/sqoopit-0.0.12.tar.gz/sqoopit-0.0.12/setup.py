# -*- coding: utf-8 -*-
'''
Author: Marco A. Gallegos
Date: 2020/02/03
Description:
this archive describes the package metadata for pypi
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqoopit",
    version="0.0.12",
    author="Marco A. Gallegos",
    author_email="ma_galeza@hotmail.com",
    description="A simple package to let you Sqoop into HDFS/Hive/HBase with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marco-gallegos/sqoopit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
