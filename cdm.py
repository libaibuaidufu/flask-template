#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/1 14:46
# @File    : cdm.py
# @author  : dfkai
# @Software: PyCharm
def run():
    """
    sqlite 不能使用
    :return:
    """
    from utils.creaet_model.createDemo import CreateApi
    from utils.creaet_model.createModels import Models
    from settings.config import create_app, db
    app = create_app(config="dev_config.py")
    headType = ["examples"]
    data = headType[0]
    with app.test_request_context():
        runmodel = Models(db, dbname="dev")
        runmodel.main(["view_example"], dataType=data)
        # craeteapi = CreateApi(db, dbname="dev")
        # craeteapi.main(["view_example"], dataType=data)


# 创建视图
from models.views.create_view import create_view

if __name__ == '__main__':
    run()
    # create_view()
