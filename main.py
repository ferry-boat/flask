from flask import session, current_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from info import create_app


# 创建应用
app = create_app("dev")
# 创建管理器
mgr = Manager(app)
# 添加迁移命令
mgr.add_command("mc", MigrateCommand)


# 生成管理员命令 先封装成函数, 再将函数包装成命令
@mgr.option("-u", dest="username")  # python main.py create_superuser -u admin -p 123456
@mgr.option("-p", dest="password")
def create_superuser(username, password):

    if not all([username, password]):
        print("参数不完整")
        return

    from info.models import User
    from info import db

    # 管理员(创建用户, is_admin=True)
    user = User()
    user.mobile = username
    user.password = password
    user.nick_name = username
    user.is_admin = True

    # 添加到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as e:
        current_app.logger.error(e)
        db.session.rollback()
        print("数据库操作错误")

    print("管理员创建成功")


if __name__ == '__main__':
    mgr.run()