from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict


# 创建数据库连接对象
db = None  # type: SQLAlchemy
sr = None  # type: StrictRedis



def create_app(config_type):  # 创建应用  工厂函数（调用者提供物料，在函数内部封装创建过程）

    # 根据类型取出配置类
    config_class = config_dict[config_type]

    app = Flask(__name__)

    # 从对象加载配置信息
    app.config.from_object(config_class)

    # 声明全局变量
    global db, sr

    # 创建数据库连接
    db = SQLAlchemy(app)
    # 创建redis连接
    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 创建Session存储对象
    Session(app)
    # 创建迁移器
    Migrate(app, db)

    # 3.注册蓝图  (如果内容只被使用一次，则可以在使用时才导入该内容)
    from info.modules.home import home_blu
    app.register_blueprint(home_blu)

    return app