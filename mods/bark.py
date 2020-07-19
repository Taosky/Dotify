import requests
from config import BARK_TOKENS


def send_message(info_dict):
    success_count = 0
    fail_count = 0

    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    for token in BARK_TOKENS:
        url =  'https://api.day.app/{}/{} {} ({}) {}分/{}'.format(token, info_dict['title'], info_dict['original_title'], info_dict['year'],info_dict['douban_rating'], info_dict['summary'])

        r = requests.get(url, headers=headers)
        if r.json()['code']==200:
            success_count += 1
        else:
            fail_count += 1
    return success_count, fail_count

