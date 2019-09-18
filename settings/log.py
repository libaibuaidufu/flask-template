#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 9:06
# @File    : log.py
# @author  : dfkai
# @Software: PyCharm
import logging.config

logging.config.fileConfig("log.conf")
logger = logging.getLogger("cse")
