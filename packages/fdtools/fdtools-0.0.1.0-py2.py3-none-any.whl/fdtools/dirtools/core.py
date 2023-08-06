# -*- coding: utf-8 -*-


"""
Directory tools
"""

__date__ = '2020-03-18'
__author__ = 'qin_hw'
__author_email__ = '1039954093@qq.com'

import os
import glob
import shutil
from os import path as osp
from functools import partial

__all__ = [
    'dirExists',
    'ensureDirExists',
    'ensureEmptyDirExists',
    'listDir',
    'parentDir',
    'pathMaker'
]


def dirExists(dir_):
    return osp.exists(dir_) and osp.isdir(dir_)


def ensureDirExists(dir_):
    """Create an empty directory if `dir_` dose not exits, or do nothing"""
    if dirExists(dir_):
        return dir_

    os.makedirs(dir_, exist_ok=True)

    return dir_


def ensureEmptyDirExists(dir_):
    """Create an empty directory or clear the exist directory"""
    if dirExists(dir_):
        shutil.rmtree(dir_)

    ensureDirExists(dir_)

    return dir_


def listDir(dir_, filenamePattern="*", fnSortKeyExtractor=None):
    fns_under_dir = glob.glob(osp.join(dir_, filenamePattern))
    fns_under_dir = sorted(fns_under_dir, key=fnSortKeyExtractor)

    return fns_under_dir


def parentDir(filename):
    return osp.abspath(os.path.join(filename, '../'))


def pathMaker(dir_):
    return partial(osp.join, dir_)
