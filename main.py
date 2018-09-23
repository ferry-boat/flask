from datetime import timedelta
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session

app = Flask(__name__)


class Config:
    # 定义和配置同名的类属性
    DEBUG = True  # 设置调试模式
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/info18"  # 设置数据库连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化
    REDIS_HOST = "127.0.0.1"  # redis的ip
    REDIS_PORT = 6379   # redis的端口
    SESSION_TYPE = "redis"  # session存储的方式
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置存储session的redis连接对象
    SESSION_USE_SIGNER = True  # 设置给sessionid进行加密， 需要设置应用秘钥
    SECRET_KEY = "Lb+Ibm1OMKQENK3+908n+OGqxgRyrvqEWiLUMgPLqOOvAEi5ZCu0rtx0/iBg973t"  # 应用秘钥
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 设置session过期时间  默认是支持过期时间



# 从对象加载配置信息
app.config.from_object(Config)

# 创建数据库连接
db = SQLAlchemy(app)
# 创建redis连接
sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 创建Session存储对象
Session(app)


@app.route('/')
def index():
    session["userid"] = 10
    return "index"


if __name__ == '__main__':
    app.run()