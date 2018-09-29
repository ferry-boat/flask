# 过滤器的本质就是函数
import functools

from flask import session, current_app, g

from info.models import User


def func_index_convert(index):
    index_dict = {1: "first", 2: "second", 3: "third"}
    return index_dict.get(index, "")


# 装饰器来封装登录信息的查询
def user_login_data(f):  # f = news_detail

    @functools.wraps(f)  # 该装饰器可以让闭包函数使用指定函数的信息
    def wrapper(*args, **kwargs):
        # 判断用户是否登录 `session中是否保存了user_id`
        user_id = session.get("user_id")
        user = None
        if user_id:  # 已登录
            # 根据`user_id`获取`用户信息
            try:
                user = User.query.get(user_id)
            except BaseException as e:
                current_app.logger.error(e)

        g.user = user

        return f(*args, **kwargs)

    return wrapper