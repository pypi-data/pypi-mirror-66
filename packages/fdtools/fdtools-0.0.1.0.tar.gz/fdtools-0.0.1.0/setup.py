# -*- coding: utf-8 -*-


__date__ = '2020-04-15'
__author__ = 'qin_hw'
__author_email__ = '1039954093@qq.com'

from setuptools import find_packages, setup

setup(
    name="fdtools",
    version="0.0.1.0",
    description="common used file and directory tools for python",
    author="qin_hw",
    author_email="1039954093@qq.com",
    license='BSD License',
    classifiers=[
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    packages=find_packages(),
    include_package_data=True,

    python_requires=">=3.0",

    install_requires=[],
)
