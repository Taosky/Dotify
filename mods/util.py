import os.path

HISTORY_FILE_PATH = '/app/data/history'

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
