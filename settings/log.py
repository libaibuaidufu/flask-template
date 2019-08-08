#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 9:06
# @File    : log.py
# @author  : dfkai
# @Software: PyCharm
import logging.config
import os

baseDir = os.getcwd()

# 日志
if not os.path.join(baseDir, "log"):
    os.mkdir(os.path.join(baseDir, "log"))
logging.config.fileConfig("log.conf")
logger = logging.getLogger("cse")
