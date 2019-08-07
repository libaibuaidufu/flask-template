#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 15:34
# @File    : view_sqlalchemy_create_example.py
# @author  : dfkai
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/31 11:54
# @File    : ExampleModelApi.py
# @author  : dfkai
# @Software: PyCharm
from sqlalchemy import Table, text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement

try:
    class CreateView(Executable, ClauseElement):
        def __init__(self, name, select):
            self.name = name
            self.select = select


    @compiles(CreateView)
    def visit_create_view(element, compiler, **kw):
        return "CREATE VIEW %s AS %s" % (
            element.name,
            compiler.process(element.select, literal_binds=True)
        )


    # test data
    from sqlalchemy import MetaData, Column, Integer
    from sqlalchemy.engine import create_engine

    engine = create_engine('sqlite:///test.sqlite')
    metadata = MetaData(engine)
    t = Table('t',
              metadata,
              Column('id', Integer, primary_key=True),
              Column('number', Integer))
    t.create()
    engine.execute(t.insert().values(id=1, number=3))
    engine.execute(t.insert().values(id=9, number=-3))

    # create view
    nel = t.select().where(t.c.id > 3)
    print(dir(t.c))
    print(nel)
    definition = text("""SELECT t.id, t.number 
    FROM t 
    WHERE t.id > 5""")
    createview = CreateView('viewname', definition)
    engine.execute(createview)

    # reflect view and print result
    v = Table('viewname', metadata, autoload=True)
    for r in engine.execute(v.select()):
        print(r)
except:
    pass
finally:
    import os
    base = os.path.join(os.path.dirname(__file__), "test.sqlite")
    os.remove(base)
