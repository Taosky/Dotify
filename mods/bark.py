import requests
from config import BARK_TOKENS
from datetime import datetime


def send_message(info_dict):
    success_count = 0
    fail_count = 0

    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}

    if int(info_dict['basic']['year']) >= datetime.now().year - 1:
        pre_title = '上新'
    else:
        pre_title = '上旧'
    title = '{}：[{}]{}（{}）'.format(pre_title, info_dict['basic']['_type'],info_dict['basic']['title'],info_dict['basic']['year'])
    for token in BARK_TOKENS:
        url =  'https://api.day.app/{}/{} {} ({}) {}分/{}'.format(token, title, info_dict['basic']['original_title'], info_dict['basic']['year'],info_dict['basic']['douban_rating'], info_dict['basic']['intro'])

        r = requests.get(url, headers=headers)
        if r.json()['code']==200:
            success_count += 1
        else:
            fail_count += 1
    return success_count, fail_count