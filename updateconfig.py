import json5
import sys
from utils import jsonDumps
from utils import updateConfig


# 迁移推送配置
def migratePush(setting, template):
    if 'push' in setting:
        return

    keys = [
        'serverChan', 'pushPlus', 'CoolPush', 'WeCom', 'Telegram',
    ]

    if 'CoolPush' in setting:
        if 'method' in setting['CoolPush']:
            setting['CoolPush']['method'] = setting['CoolPush']['method'][0]

    for key in keys:
        if key in setting and key in template['push']:
            if 'push' not in setting:
                setting['push'] = {}
            setting['push'][key] = updateConfig(setting[key], template['push'][key])
            del setting[key]


def migrateTask(setting, template):
    if 'yunbei_task' in setting:
        yunbei_task = setting['yunbei_task']
        kv = {'发布动态': '162005', '访问云音乐商城': '216002',
              '云贝推歌': '200002', '发布Mlog': '162006', '分享歌曲/歌单': '166000'}
        for key in kv:
            if key in yunbei_task and kv[key] in template['yunbei_task']:
                yunbei_task[kv[key]] = updateConfig(yunbei_task[key], template['yunbei_task'][kv[key]])
                del yunbei_task[key]

    if 'musician_task' in setting:
        musician_task = setting['musician_task']
        kv = {'登录音乐人中心': '749006', '发布动态': '740004', '发布主创说': '755000', '回复粉丝评论': '732004', '回复粉丝私信': '755001',
              '399000': '749006', '398000': '740004', '396002': '755000', '393001': '732004', '395002': '755001'}
        for key in kv:
            if key in musician_task and kv[key] in template['musician_task']:
                musician_task[kv[key]] = updateConfig(musician_task[key], template['musician_task'][kv[key]])
                del musician_task[key]
    
    if 'vip_task' in setting:
        vip_task = setting['vip_task']
        kv = {'创建共享歌单': '816', '709004': '816'}
        for key in kv:
            if key in vip_task and kv[key] in template['vip_task']:
                vip_task[kv[key]] = updateConfig(vip_task[key], template['vip_task'][kv[key]])
                del vip_task[key]


def processSetting(setting, template):
    if 'stopPushOnAPIGateway' in setting:
        del setting['stopPushOnAPIGateway']
    migratePush(setting, template)
    migrateTask(setting, template)


def before(src, dst):
    for user in src['users']:
        if 'md5' in user:
            del user['md5']
        if 'setting' in user:
            processSetting(user['setting'], dst['setting'])

    setting = src['setting']
    processSetting(setting, dst['setting'])

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
