#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 14:14
# @File    : environ.py
# @author  : dfkai
# @Software: PyCharm
import os
# 根据不同环境引入 不同 环境的app
if "dev" in os.environ.get("FLASK_SETTINGS_MODULE"):
    from app import app
else:
    from main import app