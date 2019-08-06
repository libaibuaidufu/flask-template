#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/22 15:39
# @File    : default_config.py
# @author  : dfkai
# @Software: PyCharm
import datetime

from settings.config import app


class BaseConfig():
    refresh_delta = datetime.timedelta(days=30)
    delta = datetime.timedelta(hours=10)

    DEBUG = True


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/pro'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(TestConfig)
