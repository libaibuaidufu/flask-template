#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:43
# @File    : config.py
# @author  : dfkai
# @Software: PyCharm
import os
import sys
import uuid
from datetime import datetime, date
from decimal import Decimal

# from bson.objectid import ObjectId
from flask import Flask
from flask import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache, MemcachedCache

baseDir = os.getcwd()
sys.path.insert(0, os.path.join(baseDir, "apps"))

# 日志
log_path = os.path.join(baseDir, "log")
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 缓存
try:
    cache = MemcachedCache(["ip:11211"], key_prefix="example")
except:
    cache = SimpleCache()

# 数据库
db = SQLAlchemy()

# 文件路径
UPLOAD_FOLDER = 'uploads'
TEMP_UPLOAD_FOLDER = "temps"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "doc", "docx"}


def create_app(config=None) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = uuid.uuid1()
    app.json_encoder = JSONEncoder

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_pyfile(config, silent=True)
    base_config(app)
    init_apps(app)
    register_buleprint(app)
    return app


# 注册蓝图
def register_buleprint(app):
    from apps.example import example_api
    app.register_blueprint(example_api, url_prefix="/example")


# 初始化
def init_apps(app):
    # 数据库
    db.init_app(app)


def base_config(app):
    # 文件上传配置
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16M
    app.config['UPLOAD_FOLDER'] = os.path.join(baseDir, UPLOAD_FOLDER)
    app.config['TEMP_UPLOAD_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], TEMP_UPLOAD_FOLDER)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(app.config['TEMP_UPLOAD_FOLDER']):
            os.makedirs(app.config['TEMP_UPLOAD_FOLDER'])


# json 时间 和 Decimal 格式处理
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return str(o)
        # if isinstance(o, ObjectId):
        #     return str(o)
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)
