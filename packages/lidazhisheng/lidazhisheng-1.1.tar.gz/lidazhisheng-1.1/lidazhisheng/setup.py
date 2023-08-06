# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 下午5:47
# @Author  : zyg
# @File    : setup.py
# @Desc
from distutils.core import setup
from Cython.Build import cythonize
setup(
    ext_modules = cythonize("__init__.py")
)
