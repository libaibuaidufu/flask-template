#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:58
# @File    : main.py.py
# @author  : dfkai
# @Software: PyCharm
"""
正式使用
"""

from settings.config import create_app

app = create_app(config="pro_config.py")

# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Max-Age'] = 60 * 60 * 24
#     ip = request.remote_addr
#     url = request.url
#     ip_url = ip + " : " + url
#     data = "{} {}".format(ip_url, time.time() - g.beg)
#     logger.info(data)
#     return response
#
#
# @app.before_request
# def before_request():
#     g.beg = time.time()
#     try:
#         dataDict = request.get_json()
#     except:
#         try:
#             jsonData = request.get_data()
#             dataDict = json.loads(jsonData)
#         except:
#             dataDict = {}
#     log_info = "log: " + json.dumps(dataDict)
#     logger.info(log_info)


if __name__ == '__main__':
    app.run()
