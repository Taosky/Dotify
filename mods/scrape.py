from datetime import datetime
import logging
import json
import re

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
DOUBAN_MOVIE_JSON_API = 'https://moviedb.8610000.xyz'


def get_movie_info(title, year):
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
    try:
        r = requests.post('https://dataapi.8610000.xyz/', headers={
            'api-key': 'LLppSL7L7bjMm7uHavkXOICu9iymDvwn51rADdUM7hXDjEhxVGZ8zPRqnKOdnLu8', 'Origin': 'https://moviefront.8610000.xyz', }, json=json_data)
        json_result = r.json()
        if len(json_result['documents']) > 0:
            info_json = json_result['documents'][0]
            return {
                'title': info_json['title'],
                '_type': '剧集' if info_json['is_tv'] else '电影',
                'original_title': info_json['original_title'],
                'card_subtitle': ' / '.join(info_json['tags']),
                'year': info_json['year'],
                'sharing_url': 'https://movie.douban.com/subject/{}/'.format(info_json['id']),
                'poster': info_json['poster'],
                'douban_rating': str(info_json['rating']['value']) if info_json['rating'] > 0 else '暂无'
            }
        else:
            logging.warning('未匹配到相关影视')
    except Exception as e:
        logging.warning('dataapi.8610000.xyz 请求出错')
        logging.exception(e)
    return None


def get_re_info(downloaded_dir, movie_re):
    re_result = re.match(movie_re, downloaded_dir.split('/')[-2])
    if re_result and (re_result.group(1), re_result.group(2)):
        return re_result.group(1), re_result.group(2)
    return None, None
