from info import sr
from . import home_blu
import logging  # python内置的日志模块 可以将日志信息输出到控制台，也可以将日志保存到文件中
# flask的日志信息也是用logging模块实现的，但是flask没有将日志保存到文件中
from flask import current_app, render_template


# 2.使用蓝图来注册路由
@home_blu.route('/')
def index():

    return render_template("index.html")


# 设置网站小图标
@home_blu.route('/favicon.ico')
def favicon():
    # 返回一张图标图片
    # flask中内置了语法，可以返回静态文件
    # flask中内置的访问静态文件的路由也会调用该方法
    return current_app.send_static_file("news/favicon.ico")