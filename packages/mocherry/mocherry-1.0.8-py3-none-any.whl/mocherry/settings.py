import json
import os

def load_config():
    settings_path = os.environ.get('MOCHERRY_SETTINGS_PATH')
    if settings_path is None:
        print('Sorry! No valid MoCherry project exists.')
        exit()
    else:
        with open(settings_path, 'r') as fp:
            filedata = fp.read()
            return json.loads(filedata)

CONFIG = load_config()
CONFIG['basepath'] = os.getcwd()
