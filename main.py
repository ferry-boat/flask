from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import ProductConfig

app = Flask(__name__)





# 从对象加载配置信息
app.config.from_object(ProductConfig)

# 创建数据库连接
db = SQLAlchemy(app)
# 创建redis连接
sr = StrictRedis(host=ProductConfig.REDIS_HOST, port=ProductConfig.REDIS_PORT)
# 创建Session存储对象
Session(app)
# 创建管理器
mgr = Manager(app)
# 创建迁移器
Migrate(app, db)
# 添加迁移命令
mgr.add_command("mc", MigrateCommand)


@app.route('/')
def index():
    session["userid"] = 10
    return "index"


if __name__ == '__main__':
    mgr.run()