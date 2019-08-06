#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/5 15:55
# @File    : FormatStr.py
# @author  : dfkai
# @Software: PyCharm
from flask import json
from datetime import datetime, date
from decimal import Decimal


# from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return str(o)
        # if isinstance(o, ObjectId):
        #     return str(o)
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)
