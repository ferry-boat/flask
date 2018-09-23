from info import sr
from . import home_blu


# 2.使用蓝图来注册路由
@home_blu.route('/')
def index():
    sr.set("age", 20)
    return "index"
