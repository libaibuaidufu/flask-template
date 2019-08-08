#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:43
# @File    : config.py
# @author  : dfkai
# @Software: PyCharm
import os
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache, MemcachedCache

from common.FormatStr import JSONEncoder

baseDir = os.getcwd()



# 缓存
try:
    cache = MemcachedCache(["ip:11211"], key_prefix="example")
except:
    cache = SimpleCache()

# 如 需要调用app  避免循环引用 | 如不外部引用 可放入 create_app 中
app = Flask(__name__)

# 数据库
db = SQLAlchemy()

# 文件路径
UPLOAD_FOLDER = 'static/uploads'
TEMP_UPLOAD_FOLDER = "temps"


def create_app(config=None) -> Flask:
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

    app.config["ALLOWED_EXTENSIONS"] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "doc", "docx"}
    app.config['UPLOAD_FOLDER'] = os.path.join(baseDir, UPLOAD_FOLDER)
    app.config['TEMP_UPLOAD_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], TEMP_UPLOAD_FOLDER)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(app.config['TEMP_UPLOAD_FOLDER']):
            os.mkdir(app.config['TEMP_UPLOAD_FOLDER'])
