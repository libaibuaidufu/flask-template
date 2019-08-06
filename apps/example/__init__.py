#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 11:37
# @File    : __init__.py.py
# @author  : dfkai
# @Software: PyCharm
from flask import Blueprint

example_api = Blueprint("example", __name__)

from apps.example.ExampleApi import *
