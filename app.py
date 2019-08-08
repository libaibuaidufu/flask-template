# coding:utf8
"""
测试 使用
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import *
from settings.config import create_app

app = create_app(config="dev_config.py")

# 命令管理
manager = Manager(app)
# 数据库管理
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)
# python app.py db init
# python app.py db migrate
# python app.py db upgrade

if __name__ == '__main__':
    manager.run()
