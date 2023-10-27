# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-10-27 10:24:56
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-10-27 10:48:09
# @github: https://github.com/longfengpili


import setuptools

VERSION = '0.0.1'
PROJECT_NAME = 'xinghuo'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('./requirements.txt', 'r', encoding='utf-8') as f:
    requires = f.readlines()

setuptools.setup(
    name=PROJECT_NAME,  # Replace with your own username
    version=VERSION,
    author="longfengpili",
    author_email="398745129@qq.com",
    description="A simple AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://pypi.org/project/{PROJECT_NAME}/",
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=["xinghuo", "AI"],
    python_requires=">=3.9",
    project_urls={
        'Documentation': f'https://github.com/longfengpili/{PROJECT_NAME}/blob/master/README.md',
        'Source': f'https://github.com/longfengpili/{PROJECT_NAME}',
    },
)
