from flask import current_app, abort, render_template

from info.models import News
from info.modules.news import news_blu


# 详情页面
@news_blu.route('/<int:news_id>')
def news_detail(news_id):

    # 根据新闻id查询该新闻所有的数据
    try:
        news = News.query.get(news_id)
    except BaseException as e:
        current_app.logger.error(e)
        return abort(404)

    # 将数据传入模板, 进行模板渲染
    return render_template("detail.html", news=news.to_dict())