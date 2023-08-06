#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

if sys.version_info < (3, 0):
    sys.exit('Python 3.0 or greater is required.')


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    
    def find_packages(where='.'):
        # os.walk -> list[(dirname, list[subdirs], list[files])]
        return [folder.replace("/", ".").lstrip(".")
                for (folder, _, fils) in os.walk(where)
                if "__init__.py" in fils]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyweibo_picbed',                              # 项目名称
    version="0.2.0",                                    # 项目版本号
    description=(                                       # 项目的简单描述
        'python implement of weibo picture bed.'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Superin',                                   # 作者名
    author_email='1210065650@qq.com',                   # 作者邮箱
    maintainer='Superin',                               # 维护人员名称
    maintainer_email='1210065650@qq.com',               # 维护人员邮箱
    license='MIT License',
    packages=find_packages(),
    platforms=["all"], 
    url='https://github.com/Yehrin/PyWeiboPicBed',      # Github 链接
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pycookiecheat',
        'requests',
    ]
)

