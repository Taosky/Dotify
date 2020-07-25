import json
import requests
from config import TG_CHAT_ID, TG_BOT_TOKEN, PROXY_URL, PROXY


def send_message(info_dict, url_path):
    md_text = '*{} {} （{}）*\n\n“{}” [@豆瓣]({})\n\n导演: {}\n主演: {}\n评分: {}\n路径: {} ' \
        .format(info_dict['title'], info_dict['original_title'], info_dict['year'], info_dict['summary'],
                info_dict['douban_url'], info_dict['directors'], info_dict['casts'],
                info_dict['douban_rating'], url_path, )

    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TG_BOT_TOKEN)
    data = {'chat_id': TG_CHAT_ID, 'text': md_text, 'parse_mode': 'markdown'}

    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}

    try:
        if PROXY:
            r = requests.post(url, headers=headers, data=json.dumps(
                data), proxies={'http': PROXY_URL, 'https': PROXY_URL})
        else:
            r = requests.post(url, headers=headers, data=json.dumps(data))
    except:
        return None
    return r.json()['ok']
