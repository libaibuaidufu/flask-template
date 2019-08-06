#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 15:31
# @File    : create_view.py
# @author  : dfkai
# @Software: PyCharm
"""
创建视图
"""
from sqlalchemy import text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement

from settings.config import create_app, db


class CreateView(Executable, ClauseElement):
    def __init__(self, name, select):
        self.name = name
        self.select = select


@compiles(CreateView)
def visit_create_view(element, compiler, **kw):
    return "CREATE VIEW IF NOT EXISTS %s AS %s" % (
        element.name,
        compiler.process(element.select, literal_binds=True)
    )


# create_view
def create_view():
    """
    创建视图
    :return:
    """
    app = create_app(config="dev_config.py")
    definition = text("""select * from site_channel where id>=1""")
    with app.app_context():
        createview = CreateView('view_site_channel', definition)
        db.engine.execute(createview)
