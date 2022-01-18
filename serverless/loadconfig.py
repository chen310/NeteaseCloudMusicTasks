import json5
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from utils import jsonDumps
from utils import updateConfig


# 迁移推送配置
def migratePush(setting):
    if 'push' in setting:
        return

    keys = [
        'serverChan', 'pushPlus', 'CoolPush', 'WeCom', 'Telegram',
    ]

    if 'CoolPush' in setting:
        if 'method' in setting['CoolPush']:
            setting['CoolPush']['method'] = setting['CoolPush']['method'][0]

    for key in keys:
        if key in setting:
            if 'push' not in setting:
                setting['push'] = {}
            setting['push'][key] = setting[key]
            del setting[key]


def before(src, dst):
    for user in src['users']:
        if 'md5' in user:
            del user['md5']
        if 'setting' in user:
            migratePush(user['setting'])

    setting = src['setting']
    migratePush(setting)

    if 'stopPushOnAPIGateway' in setting:
        del setting['stopPushOnAPIGateway']

    key_list = ['version', 'desp']
    for key in key_list:
        if key in dst:
            src[key] = dst[key]
        else:
            if key in src:
                del src[key]


with open(sys.argv[1], 'r', encoding='utf-8') as f:
    config = json5.load(f)
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    oldconfig = json5.load(f)

before(oldconfig, config)

data = updateConfig(oldconfig, config)

with open(sys.argv[3], 'w', encoding='utf-8') as f:
    f.write(jsonDumps(data))
