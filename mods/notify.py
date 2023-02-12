import requests
import json
import logging
import urllib

TG_HEADERS = {'Content-Type': 'application/json',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}

BARK_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}

TG_API_PROXY = 'https://tapi.taosky.eu.org'


def send_tg(info_dict, url_path, chat_id, bot_token):
    logging.info('开始telegram推送...')
    md_text = '*{} {}*\n\n“{}” [@豆瓣]({})\n\n{}\n\n豆瓣评分 {}\n\n{} ' \
        .format(info_dict['title'], info_dict['original_title'], info_dict['intro'],
                info_dict['sharing_url'], info_dict['card_subtitle'],
                info_dict['douban_rating'], url_path, )

    url = '{}/bot{}/sendMessage'.format(TG_API_PROXY, bot_token)
    data = {'chat_id': chat_id, 'text': md_text, 'parse_mode': 'markdown'}

    try:
        r = requests.post(url, headers=TG_HEADERS, data=json.dumps(data))
    except:
        return None
    return r.json()['ok']


def send_bark(info_dict, tokens):
    logging.info('开始bark推送...')
    success_count = 0
    fail_count = 0
    title = '{} {} （豆瓣评分 {}）'.format(
        info_dict['title'], info_dict['original_title'], info_dict['douban_rating'])
    content = info_dict['card_subtitle']
    for token in tokens:
        if not token or token == '':
            continue
        url = 'https://api.day.app/{}/{}/{}'.format(
            token,
            urllib.parse.quote(title, encoding='utf-8',
                               safe='', errors='replace'),
            urllib.parse.quote(content, encoding='utf-8', safe='', errors='replace'))
        r = requests.get(url, headers=BARK_HEADERS)
        logging.info(r.text)
        if r.json()['code'] == 200:
            success_count += 1
        else:
            fail_count += 1
    return success_count, fail_count
