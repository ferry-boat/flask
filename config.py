import logging
from datetime import timedelta
from redis import StrictRedis


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


class DevelopmentConfig(Config):  # 开发环境配置
    DEBUG = True  # 设置调试模式
    LOG_LEVEL = logging.DEBUG


class ProductConfig(Config):  # 生产环境配置
    DEBUG = False  # 设置调试模式
    LOG_LEVEL = logging.ERROR


config_dict = {
    "dev": DevelopmentConfig,
    "pro": ProductConfig
}