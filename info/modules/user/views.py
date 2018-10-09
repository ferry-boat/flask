from info.common import user_login_data
from info.modules.user import user_blu
from flask import render_template, g, redirect


# 显示个人中心
@user_blu.route('/user_info')
@user_login_data
def user_info():
    # 判断用户是否登录

    user = g.user
    if not user:
        return redirect("/")

    return render_template("user.html", user=user.to_dict())