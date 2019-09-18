#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:58
# @File    : main.py.py
# @author  : dfkai
# @Software: PyCharm
"""
正式使用
"""
import os

from settings.config import create_app

os.environ.setdefault("FLASK_SETTINGS_MODULE", "pro_config.py")

app = create_app(config="pro_config.py")


@app.after_request
def after_request(response):
    response.headers['Access-Control-Max-Age'] = 60 * 60 * 24
    return response


if __name__ == '__main__':
    app.run()
