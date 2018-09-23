from info import sr
from . import home_blu
import logging  # python内置的日志模块 可以将日志信息输出到控制台，也可以将日志保存到文件中
# flask的日志信息也是用logging模块实现的，但是flask没有将日志保存到文件中
from flask import current_app


# 2.使用蓝图来注册路由
@home_blu.route('/')
def index():
    try:
        a = 10 / 0
    except BaseException as e:
        # logging.error(e)  # 默认的输出不显示错误位置， 建议使用flask内置的语法
        current_app.logger.error(e)

    return "index"
