import re

import mods.bark as bk
import mods.telegram as tg
from config import API_TOKENS, BARK_ON, MOVIE_DIR_RE, TG_ON
from flask import Flask, render_template, request
from mods.douban import get_db_id2, get_db_info, login

app = Flask(__name__)

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'

S = login()


def check_db_logout():
    global S
    url = 'https://www.douban.com/mine/'
    ua_headers = {"User-Agent": UA}
    r = S.get(url, headers=ua_headers)
    if r.headers.get('Location') == 'https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/mine/':
        S = login()


def get_movie(name, year):
    print('\n{}({})'.format(name, year))
    check_db_logout()
    if S:
        print('豆瓣登录状态正常\n')
    else:
        print('豆瓣登录失败...\n')
        return None
    db_id = get_db_id2(S, name, year)
    if not db_id:
        print('获取豆瓣Subject ID错误')
        return None
    db_info = get_db_info(S, db_id)

    return db_info


@app.route('/')
def index():

    return 'Hello'


@app.route('/downloaded')
def downloaded():
    downloaded_dir = request.args.get('dir')
    token = request.args.get('token')

    if not downloaded_dir or token not in API_TOKENS:
        res_result = '参数错误'
        return res_result

    re_result = re.match(MOVIE_DIR_RE, downloaded_dir.split('/')[-2])
    if re_result and (re_result.group(1), re_result.group(2)):
        db_info = get_movie(re_result.group(1), re_result.group(2))
        res_result = '{}（{}）\n'.format(re_result.group(1), re_result.group(2))
        if not db_info:
            res_result += '豆瓣: 获取信息错误\n'
            return res_result

        if TG_ON:
            tg_result = tg.send_message(db_info, downloaded_dir)
            res_result += 'Telegram: 发送成功\n' if tg_result else 'Telegram: 发送失败\n'
        if BARK_ON:
            bark_success_count, bark_fail_count = bk.send_message(db_info)
            res_result += 'Bark: {}成功,{}失败\n'.format(bark_success_count, bark_fail_count)
    else:
        res_result = '无法识别\n'

    return res_result





if __name__ == '__main__':
    app.run('0.0.0.0')
