from datetime import datetime
import logging
import json
import re

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
DOUBAN_MOVIE_JSON_API = 'https://moviedb.8610000.xyz'


def get_movie_id(title, year):
    json_data = {
        'collection': 'movie',
        'database': 'Douban',
        'dataSource': 'Cluster0',
        'filter': {
            'title': {
                '$regex': title,
                '$options': 'i',
            },
            'year': str(year)
        },
        'sort': {
            'year': -1,
            '_id': -1,
        },
        'skip': 0,
        'limit': 10,
    }
    mid = None
    try:
        r = requests.post('https://dataapi.8610000.xyz/', headers={
            'api-key': 'LLppSL7L7bjMm7uHavkXOICu9iymDvwn51rADdUM7hXDjEhxVGZ8zPRqnKOdnLu8', 'Origin': 'https://moviefront.8610000.xyz', }, json=json_data)
        json_result = r.json()
        if len(json_result['documents']) > 0:
            mid = json_result['documents'][0]['id']
        else:
            logging.warning('未匹配到相关影视')
    except Exception as e:
        logging.warning('dataapi.8610000.xyz 请求解析出错')
        logging.exception(e)
    return mid


def get_re_info(downloaded_dir, movie_re):
    re_result = re.match(movie_re, downloaded_dir.split('/')[-2])
    if re_result and (re_result.group(1), re_result.group(2)):
        return re_result.group(1), re_result.group(2)
    return None, None


def get_movie_info(title, year):
    logging.info('开始抓取 {} ...'.format(title))

    mid = get_movie_id(title, year)
    if not mid:
        return None

    url = DOUBAN_MOVIE_JSON_API + '/data/{}.json'.format(mid)
    try:
        r = requests.get(url, headers=HEADERS)
        r.encoding = 'utf-8'
        info_json = json.loads(r.text)
    except Exception as e:
        logging.warning('{}请求解析出错'.format(DOUBAN_MOVIE_JSON_API))
        logging.exception(e)
        return None
    return {
        'title': info_json['title'],
        '_type': '剧集' if info_json['episodes_count'] else '电影',
        'original_title': info_json['original_title'],
        'intro': info_json['intro'] if 'intro' in info_json and info_json['intro'] else '',
        'card_subtitle': info_json['card_subtitle'] if 'card_subtitle' in info_json and info_json['card_subtitle'] else '',
        'year': info_json['year'],
        'update_date': datetime.now(),
        'sharing_url': info_json['sharing_url'],
        'cover_url': info_json['cover_url'] if 'cover_url' in info_json and info_json['cover_url'] else info_json['pic']['normal'],
        'douban_rating': str(info_json['rating']['value']) if info_json['rating'] else '暂无'
    }
