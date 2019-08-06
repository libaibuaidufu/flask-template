#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:47
# @File    : pro_config.py
# @author  : dfkai
# @Software: PyCharm
import datetime
import os
baseDir = os.getcwd()
pro_db = rf"{os.path.join(baseDir,'settings/pro.db')}"
refresh_delta = datetime.timedelta(days=30)
delta = datetime.timedelta(hours=10)

DEBUG = False

# db
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/pro?charset=utf8'
SQLALCHEMY_DATABASE_URI = f'sqlite:///{pro_db}'
SQLALCHEMY_TRACK_MODIFICATIONS = True
