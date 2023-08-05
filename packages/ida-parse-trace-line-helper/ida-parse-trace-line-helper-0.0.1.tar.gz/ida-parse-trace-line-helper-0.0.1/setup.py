# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ida-parse-trace-line-helper",
    version="0.0.1",
    author="beyond_mark",
    author_email="luck.yangbo@gmail.com",
    description="parse trace file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BeyondMark/ida-parse-trace-file-helper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

