# -*- coding: utf-8 -*-


"""
Some file tools
"""

__date__ = '2020-03-18'
__author__ = 'qin_hw'
__author_email__ = '1039954093@qq.com'

import os
from os import path as osp

__all__ = [
    'fileExists',
    'ensureFileExists',
    'ensureEmptyFileExists',
    'fileName',
    'fileSuffix',
]


def fileExists(filename):
    return osp.exists(filename) and osp.isfile(filename)


def ensureFileExists(filename):
    if fileExists(filename):
        return filename

    with open(filename, 'r+') as _:
        pass

    return filename


def ensureEmptyFileExists(filename):
    if fileExists(filename):
        os.remove(filename)

    ensureEmptyFileExists(filename)

    return filename


def fileName(path_, withSuffix=True):
    filename = osp.basename(path_)
    filename = filename if withSuffix else filename[:filename.rfind('.')]

    return filename


def fileSuffix(filename):
    return os.path.splitext(filename)[-1][1:].lower()
