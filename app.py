import re
import mods.bark as bk
import mods.telegram as tg
import mods.umeng as um
from config import API_TOKEN, BARK_ON, MOVIE_DIR_RE, TG_ON, UMENG_ON
from flask import Flask, render_template, request, jsonify
from mods.douban import get_movie
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.WARNING)


@app.route('/')
def index():
    return render_template('index.html', API_TOKEN=API_TOKEN)


@app.route('/downloaded')
def downloaded():
    downloaded_dir = request.args.get('dir')
    token = request.args.get('token')

    if not downloaded_dir or token != API_TOKEN:
        return jsonify({'msg': '未授权', 'code':403}), 403
    
    if '/' not in downloaded_dir:
        re_result = re.match(MOVIE_DIR_RE, downloaded_dir)
    else:
        re_result = re.match(MOVIE_DIR_RE, downloaded_dir.split('/')[-2])

    if re_result and (re_result.group(1), re_result.group(2)):
        res_result = ''
        db_info = get_movie(re_result.group(1), re_result.group(2))
        if not db_info:
            return jsonify({'msg': '{}（{}）：获取豆瓣信息出错'.format(re_result.group(1), re_result.group(2)), 'code': 400}), 400
        if TG_ON:
            tg_result = tg.send_message(db_info, downloaded_dir)
            res_result += 'Telegram发送成功, ' if tg_result else 'Telegram: 发送失败, '
        if BARK_ON:
            bark_success_count, bark_fail_count = bk.send_message(db_info)
            res_result += 'Bark{}成功{}失败, '.format(bark_success_count, bark_fail_count)
        if UMENG_ON:
            umeng_result = um.send_message(db_info)
            res_result += '友盟发送成功' if umeng_result.status_code==200 else '友盟发送失败'
        return jsonify({'msg': res_result, 'code': 200}), 200
    else:

         return jsonify({'msg': '无法识别', 'code': 400}), 400

    return res_result


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)