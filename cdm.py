#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 14:46
# @File    : cdm.py
# @author  : dfkai
# @Software: PyCharm
from models.views.create_view import create_view
from unup.creaet_model.createDemo import CreateApi
from unup.creaet_model.createModels import Models
from settings.config import create_app, db


def run():
    """
    sqlite 不能使用
    :return:
    """
    app = create_app(config="dev_config.py")
    headType = ["examples"]
    data = headType[0]
    with app.test_request_context():
        runmodel = Models(db, dbname="dev")
        runmodel.main(["view_example"], dataType=data)
        # craeteapi = CreateApi(db, dbname="dev")
        # craeteapi.main(["view_example"], dataType=data)


if __name__ == '__main__':
    run()
