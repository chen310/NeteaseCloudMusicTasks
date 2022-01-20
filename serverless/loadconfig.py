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


def migrateTask(setting):
    if 'yunbei_task' in setting:
        yunbei_task = setting['yunbei_task']
        kv = {'发布动态': '162005', '访问云音乐商城': '216002',
              '云贝推歌': '200002', '发布Mlog': '162006', '分享歌曲/歌单': '166000'}
        for key in kv:
            if key in yunbei_task:
                yunbei_task[kv[key]] = yunbei_task[key]
                del yunbei_task[key]

    if 'musician_task' in setting:
        musician_task = setting['musician_task']
        kv = {'登录音乐人中心': '399000', '发布动态': '398000',
              '发布主创说': '396002', '回复粉丝评论': '393001', '回复粉丝私信': '395002'}
        for key in kv:
            if key in musician_task:
                musician_task[kv[key]] = musician_task[key]
                del musician_task[key]


def processSetting(setting):
    if 'stopPushOnAPIGateway' in setting:
        del setting['stopPushOnAPIGateway']
    migratePush(setting)
    migrateTask(setting)


def before(src, dst):
    for user in src['users']:
        if 'md5' in user:
            del user['md5']
        if 'setting' in user:
            processSetting(user['setting'])

    setting = src['setting']
    processSetting(setting)

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
