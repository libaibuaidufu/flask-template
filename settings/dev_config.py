#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:46
# @File    : dev_config.py
# @author  : dfkai
# @Software: PyCharm
import datetime
import os

baseDir = os.getcwd()
dev_db = rf"{os.path.join(baseDir, 'settings/dev.sqlite')}"
refresh_delta = datetime.timedelta(days=30)
delta = datetime.timedelta(hours=10)

DEBUG = True

# db
SQLALCHEMY_DATABASE_URI = f'sqlite:///{dev_db}'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/dev?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
