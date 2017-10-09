# -*- coding: utf-8 -*-
# @Author: caixin
# @Date:   2017-09-29 16:47:24
# @Last Modified by:   1249614072@qq.com
# @Last Modified time: 2017-09-29 16:55:41
"""
Python 2.6, 2.7, and 3.x compatibility.

"""
import sys
import types


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
