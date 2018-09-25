from info import sr
from info.modules.passport import passport_blu
from flask import request, abort, current_app, make_response, Response

# 获取图片验证码
from info.utils.captcha.pic_captcha import captcha


@passport_blu.route('/get_img_code')
def get_img_code():
    # 获取参数
    img_code_id = request.args.get("img_code_id")
    # 校验参数
    if not img_code_id:
        return abort(403)

    # 生成图片验证码
    img_name, img_text, img_bytes = captcha.generate_captcha()

    # 保存图片key和验证码文字  redis 方便设置过期时间
    try:
        sr.set("img_code_id"+img_code_id, img_text, ex=180)
    except BaseException as e:
        current_app.logger.error(e)

    # 设置自定义的响应头， 必须手动创建响应对象
    response = make_response(img_bytes)  # type: Response
    response.content_type = "image/jpeg"
    # 返回验证码图片
    return response