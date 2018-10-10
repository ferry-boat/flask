from flask import render_template, request, current_app, redirect, url_for

from info.models import User
from info.modules.admin import admin_blu


# 后台登录
@admin_blu.route('/login', methods=['GET', "POST"])
def login():

    if request.method == 'GET': # 显示页面
        return render_template("admin/login.html")

    # POST处理
    username = request.form.get("username")
    password = request.form.get("password")

    if not all([username, password]):
        return render_template("admin/login.html", errmsg="参数不完整")

    # 取出用户模型
    try:
        user = User.query.filter(User.mobile==username, User.is_admin==True).first()
    except BaseException as e:
        current_app.logger.error(e)
        return render_template("admin/login.html", errmsg="数据库错误")

    if not user:
        return render_template("admin/login.html", errmsg="该管理员不存在")

    # 校验密码
    if not user.check_password(password):
        return render_template("admin/login.html", errmsg="用户名/密码错误")

    # 重定向到后台首页
    return redirect(url_for("admin.index"))



# 后台首页
@admin_blu.route('/index')
def index():

    return render_template("admin/index.html")