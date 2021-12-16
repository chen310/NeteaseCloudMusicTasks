# -*- coding: utf-8 -*-
import requests
import json
import json5
import re
from user import User
from wecom import WeComAlert


def md2text(data):
    data = re.sub(r'\n\n', r'\n', data)
    data = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1: \2 ', data)
    data = re.sub(r'- ', r'  ➢ ', data)
    data = re.sub(r'#### (.*?)\n', r'【\1】\n', data)
    data = re.sub(r'### ', r'\n', data)
    data = re.sub(r'用户(\d+)', r'用户\1', data)
    return data


def start(event, context):
    config = json5.load(open('./config.json', 'r', encoding='utf-8'))
    setting = config['setting']

    user_count = 0

    SCKEYs = {}
    Skeys = {}
    pushToken = {}

    res = ''
    for user_config in config['users']:
        user_count += 1

        user_setting = setting
        if "setting" in user_config:
            for key in user_config['setting']:
                user_setting[key] = user_config['setting'][key]

        user = User()
        user.setUser(username=user_config['username'], password=user_config['password'], isMd5=user_config['md5'],
                     countrycode=user_config.get('countrycode', ''), user_setting=user_setting, No=user_count, ip=user_config['X-Real-IP'])
        if user.isLogined:
            user.userInfo()

            if user_setting['follow']:
                user.follow()

            if user_setting['sign']:
                user.sign()

            task_on = False
            tasks = user_setting['yunbei_task']
            for task in user_setting['yunbei_task']:
                task_on = task_on or tasks[task]['enable']
            if task_on:
                user.yunbei_task()

            user.get_yunbei()

            if user.userType == 4:
                user.musician_task()

            if user.vipType == 11:
                user.vip_task()

            if user_setting['daka']['enable']:
                user.daka()

            if user_setting['other']['play_playlists']['enable']:
                user.play_playlists()

        res += user.msg
        # user.msg = user.msg.strip()

        # API网关访问
        if 'requestContext' in event and user_setting.get('noPushOnAPIGateway', True):
            continue

        sckey = user_setting['serverChan']['KEY']
        if user_setting['serverChan']['enable'] and len(sckey) > 0:
            if sckey in SCKEYs:
                SCKEYs[sckey]['msg'] += user.msg
            else:
                SCKEYs[sckey] = {'title': user.title, 'msg': user.msg}

        skey = user_setting['CoolPush']['Skey']
        if user_setting['CoolPush']['enable'] and len(skey) > 0:
            if skey in Skeys:
                Skeys[skey]['msg'] += user.msg
            else:
                Skeys[skey] = {
                    'title': user.title, 'method': user_setting['CoolPush']['method'], 'msg': user.msg}

        pushtoken = user_setting['pushPlus']['pushToken']
        if user_setting['pushPlus']['enable'] and len(pushtoken) > 0:
            # 一对多单独发送
            if len(user_setting['pushPlus']['topic']) > 0:
                push_url = 'http://www.pushplus.plus/send'
                data = {
                    "token": pushtoken,
                    "title": user.title,
                    "content": user.msg,
                    "topic": user_setting['pushPlus']['topic']
                }
                body = json.dumps(data).encode(encoding='utf-8')
                headers = {'Content-Type': 'application/json'}
                requests.post(push_url, data=body, headers=headers)
            else:
                if pushtoken in pushToken:
                    pushToken[pushtoken]['msg'] += user.msg
                else:
                    pushToken[pushtoken] = {
                        'title': user.title, 'msg': user.msg}

        if user_setting['WeCom']['enable'] and len(user_setting['WeCom']['corpid']) > 0 and len(user_setting['WeCom']['secret']) > 0 and len(user_setting['WeCom']['agentid']) > 0:
            alert = WeComAlert(
                user_setting['WeCom']['corpid'], user_setting['WeCom']['secret'], user_setting['WeCom']['agentid'])
            msg = user.msg
            if user_setting['WeCom']['msgtype'] != 'markdown':
                msg = md2text(msg)
            alert.send_msg(user_setting['WeCom']['userid'], user_setting['WeCom']['msgtype'],
                           msg, "网易云音乐打卡", 'https://music.163.com/#/user/home?id='+str(user.uid))

    if 'requestContext' in event and user_setting.get('noPushOnAPIGateway', True):
        return res

    for sckey in SCKEYs:
        serverChan_url = ''
        if sckey.startswith('SCT'):
            serverChan_url = 'https://sctapi.ftqq.com/'+sckey+'.send'
        else:
            serverChan_url = 'https://sc.ftqq.com/'+sckey+'.send'
        requests.post(serverChan_url, data={
                      "text": SCKEYs[sckey]['title'], "desp": SCKEYs[sckey]['msg']})

    for skey in Skeys:
        for method in Skeys[skey]['method']:
            CoolPush_url = "https://push.xuthus.cc/{}/{}".format(method, skey)
            if method == "email":
                requests.post(CoolPush_url, data={
                              "t": Skeys[skey]['title'], "c": md2text(Skeys[skey]['msg'])})
            else:
                requests.get(CoolPush_url, params={"c": Skeys[skey]['msg']})

    # Pushplus推送
    for pushtoken in pushToken:
        push_url = 'http://www.pushplus.plus/send'
        data = {
            "token": pushtoken,
            "title": pushToken[pushtoken]['title'],
            "content": pushToken[pushtoken]['msg']
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        requests.post(push_url, data=body, headers=headers)

    return res


def main_handler(event, context):
    res = start(event, context)
    if 'requestContext' in event:
        data = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": "<html lang=\"zh-CN\"><meta charset=\"utf-8\"><body><p>" + "<br />" + md2text(res).replace("\n", "<br />") + "</p></body></html>"
        }
        return data


if __name__ == '__main__':
    start({}, {})
