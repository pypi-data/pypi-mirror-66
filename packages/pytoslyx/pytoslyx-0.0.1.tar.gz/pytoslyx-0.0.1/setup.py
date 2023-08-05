#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/4/17 2:57 下午
# @Author : lianyongxing
# @E-mail : lianyongxing@bytedance.com
# @Site : Shanghai
# @File : setup.py.py
# @Description: None

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytoslyx",
    version="0.0.1",
    author="lianyongxing",
    author_email="yxlian@sjtu.edu.cn    ",
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)