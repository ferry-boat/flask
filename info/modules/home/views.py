from info import sr
from . import home_blu
import logging  # python内置的日志模块 可以将日志信息输出到控制台，也可以将日志保存到文件中
# flask的日志信息也是用logging模块实现的，但是flask没有将日志保存到文件中
from flask import current_app, render_template


# 2.使用蓝图来注册路由
@home_blu.route('/')
def index():

    return render_template("index.html")
