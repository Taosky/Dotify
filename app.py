import os
import logging
from mods.notify import send_bark, send_tg
from flask import Flask, request, jsonify
from mods.scrape import get_movie_info, get_re_info
from mods.util import read_history, write_history, history_file_exists

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

MOVIE_DIR_RE = os.getenv('MOVIE_DIR_RE') if os.getenv(
    'MOVIE_DIR_RE') else '(.*?)（(\d{4})）'
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
BARK_TOKENS = os.getenv('BARK_TOKENS')
PATH_DELETE = os.getenv('PATH_DELETE')
PATH_ADD = os.getenv('PATH_ADD')

app = Flask(__name__)


@app.route('/downloaded')
def downloaded():
    downloaded_dir = request.args.get('dir')
    if PATH_DELETE:
        downloaded_dir = downloaded_dir.lstrip(PATH_DELETE)
    if PATH_ADD:
        downloaded_dir = PATH_ADD + downloaded_dir

    if not downloaded_dir:
        return jsonify({'code': 900, 'msg': '缺少参数'}), 900
    logging.info(downloaded_dir.split('/')[-2])

    title, year = get_re_info(downloaded_dir, MOVIE_DIR_RE)
    
    if not title or not year:
        return jsonify({'code': 901, 'msg': '文件名解析错误'}), 901
    
    movie_str = title + ',' + year

    if history_file_exists() and movie_str in read_history():
        return jsonify({'code': 800, 'msg': '已提交过'}), 800

    db_info = get_movie_info(title, year)
    if not db_info:
        return jsonify({'code': 902, 'msg': '数据抓取错误'}), 902

    write_history(movie_str)

    result_msg = ''
    if TG_BOT_TOKEN and TG_CHAT_ID:
        tg_result = send_tg(db_info, downloaded_dir, TG_CHAT_ID, TG_BOT_TOKEN)
        result_msg += 'Telegram 发送'
        if not tg_result:
            result_msg += '失败; '
        else:
            result_msg += '成功; '
    if BARK_TOKENS and '_' in BARK_TOKENS:
        bark_success_count, bark_fail_count = send_bark(
            db_info, BARK_TOKENS.split('_'))
        result_msg += 'Bark 发送 '
        result_msg += '成功: {}, 失败: {}; '.format(
            bark_success_count, bark_fail_count)

    return jsonify({'code': 200, 'msg': result_msg}), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 4023)
