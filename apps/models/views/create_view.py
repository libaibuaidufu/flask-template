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
from sqlalchemy.sql.ddl import DropTable
from sqlalchemy.sql.expression import Executable, ClauseElement

from settings.config import create_app, db


class CreateView(Executable, ClauseElement):
    def __init__(self, name, select):
        self.name = name
        self.select = select


@compiles(CreateView)
def visit_create_view(element, compiler, **kw):
    return "CREATE VIEW  %s AS %s" % (
        element.name,
        compiler.process(element.select, literal_binds=True)
    )


# create_view
def create_view(sql, view_name):
    """
    创建视图
    :return:
    """
    app = create_app(config="dev_config.py")
    definition = text(sql)
    with app.app_context():
        createview = CreateView(view_name, definition)
        db.engine.execute(createview)


@compiles(DropTable)
def _compile_drop_table(element, compiler, **kwargs):
    if hasattr(element.element, 'is_view') and element.element.is_view:
        return compiler.visit_drop_view(element)
    # cascade seems necessary in case SQLA tries to drop
    # the table a view depends on, before dropping the view
    return compiler.visit_drop_table(element) + ' CASCADE'
