import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, g
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict


# 创建数据库连接对象
db = None  # type: SQLAlchemy
sr = None  # type: StrictRedis


def setup_log(log_level):  # 将日志保存到文件中
    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(pathname)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)



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
    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)
    # 创建Session存储对象
    Session(app)
    # 创建迁移器
    Migrate(app, db)

    # 3.注册蓝图  (如果内容只被使用一次，则可以在使用时才导入该内容)
    from info.modules.home import home_blu
    app.register_blueprint(home_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    from info.modules.user import user_blu
    app.register_blueprint(user_blu)

    from info.modules.admin import admin_blu
    app.register_blueprint(admin_blu)

    # 配置日志
    setup_log(config_class.LOG_LEVEL)

    # 关联模型文件
    # from info.models import *  # 函数和方法内部不允许该语法
    import info.models

    # 添加过滤器
    from info.common import func_index_convert
    app.add_template_filter(func_index_convert, "index_convert")


    from info.common import user_login_data
    # 捕获404异常
    @app.errorhandler(404)
    @user_login_data
    def error_handle_404(error):  # 必须设置参数接收异常信息
        user = g.user
        user = user.to_dict() if user else None
        # 模板渲染404页面
        return render_template("news/404.html", user=user)

    return app