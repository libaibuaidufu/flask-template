# coding:utf8
"""
测试 使用
"""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import CreateTable

from settings.config import create_app, db

os.environ.setdefault("FLASK_SETTINGS_MODULE", "dev_config.py")

app = create_app(config="dev_config.py")

#
# @compiles(CreateTable)
# def visit_create_table(element, compiler, **kw):
#     if hasattr(element.element, 'is_view') and element.element.is_view:
#         print("fuck")
#         pass
#     else:
#         return compiler.visit_create_table(element)

# 命令管理
manager = Manager(app)
# 数据库管理
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@migrate.configure
def configure_alembic(config):
    print(config)
    print(dir(config))
    # modify config object
    return config


# python app.py db init
# python app.py db migrate
# python app.py db upgrade


if __name__ == '__main__':
    manager.run()
