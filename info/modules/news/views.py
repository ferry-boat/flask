from flask import current_app, abort, render_template, g, request, jsonify

from info.common import user_login_data
from info.constants import CLICK_RANK_MAX_NEWS
from info.models import News
from info.modules.news import news_blu
from info.utils.response_code import RET, error_map


# 详情页面
@news_blu.route('/<int:news_id>')
@user_login_data  #  news_detail = user_login_data(news_detail)
def news_detail(news_id):

    # 根据新闻id查询该新闻所有的数据
    try:
        news = News.query.get(news_id)
    except BaseException as e:
        current_app.logger.error(e)
        return abort(404)

    # 点击量+1
    news.clicks += 1

    # 查询`点击量排行前10的新闻`
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(CLICK_RANK_MAX_NEWS).all()
    except BaseException as e:
        current_app.logger.error(e)

    news_list = [news.to_basic_dict() for news in news_list]

    user = g.user.to_dict() if g.user else None

    # 将数据传入模板, 进行模板渲染
    return render_template("detail.html", news=news.to_dict(), news_list=news_list, user=user)



# 新闻收藏
@news_blu.route('/news_collect', methods=['POST'])
@user_login_data
def news_collect():
    # 判断用户是否登录
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg=error_map[RET.SESSIONERR])
    
    # 获取参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    # 校验参数
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    try:
        news_id = int(news_id)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    # 判断该新闻是否存在
    try:
        news = News.query.get(news_id)
    except BaseException as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

    if not news:
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    if action not in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    # 根据action执行收藏/取消收藏(user和news建立/删除关系)
    if action == "collect": # 收藏
        # 让user和news建立关系
        user.collection_news.append(news)
    else:  # 取消收藏
        user.collection_news.remove(news)

    # json返回结果
    return jsonify(errno=RET.OK, errmsg=error_map[RET.OK])