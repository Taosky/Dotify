import time
import json
import os.path

import requests

Q_FILE_PATH = '/app/data/q.cache'
HISTORY_FILE_PATH = '/app/data/history'

Q_FILE_URL = 'https://gitlab.com/Taosky/partfork/-/raw/master/q.json'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}


def history_file_exists():
    return os.path.exists(HISTORY_FILE_PATH)


def read_history():
    history_list = []
    with open(HISTORY_FILE_PATH) as f:
        for line in f.readlines():
            history_list.append(line.strip('\n'))

    return history_list


def write_history(info):
    with open(HISTORY_FILE_PATH, 'a') as f:
        f.write('\n'+info)


def q_file_exists():
    return os.path.exists(Q_FILE_PATH)


def q_file_expired():
    filemt = time.mktime(time.localtime(os.stat(Q_FILE_PATH).st_mtime))
    return time.time() - filemt > 18000


def download_q_file():
    with requests.get(Q_FILE_URL, headers=HEADERS, stream=True,  timeout=100) as r:
        with open(Q_FILE_PATH, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


def read_q_file():
    with open(Q_FILE_PATH) as f:
        text = f.read()
    return json.loads(text)
