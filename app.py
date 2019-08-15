# coding:utf8
"""
测试 使用
"""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.models import *
from settings.config import create_app, db

os.environ.setdefault("FLASK_SETTINGS_MODULE", "dev_config.py")

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
