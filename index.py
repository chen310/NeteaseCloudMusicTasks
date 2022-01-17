# -*- coding: utf-8 -*-
from utils import updateConfig
import time
import requests
import json
import json5
import re
import os
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


def getSongNumber():
    res = {}
    if "SONG_NUMBER" in os.environ:
        sp1 = os.environ.get("SONG_NUMBER").split("#")
        if len(sp1) != 2:
            return res
        if sp1[0] != time.strftime("%Y-%m-%d", time.gmtime(time.time()+28800)):
            print("环境变量 SONG_NUMBER 已过期")
            return res
        for number in sp1[1].split(";"):
            sp2 = number.split(":")
            if len(sp2) == 2:
                res[sp2[0]] = int(sp2[1])
    return res


def start(event={}, context={}):
    with open('./config.json', 'r', encoding='utf-8') as f:
        config = json5.load(f)
    setting = config['setting']

    user_count = 0

    SCKEYs = {}
    Skeys = {}
    pushToken = {}
    tgkeys = {}

    res = ''
    songnumber = getSongNumber()
    for user_config in config['users']:
        if user_config['enable'] == False:
            continue
        user_count += 1

        if "setting" in user_config:
            user_setting = updateConfig(user_config["setting"], setting)
        else:
            user_setting = setting

        user = User()
        user.setUser(username=user_config['username'], password=user_config['password'], countrycode=user_config.get(
            'countrycode', ''), user_setting=user_setting, No=user_count, ip=user_config['X-Real-IP'])
        if user.isLogined:
            user.songnumber = songnumber.get(str(user.uid), -1)
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
                if user_setting['daka']['auto'] == True and user.songnumber != -1:
                    user.auto_daka()
                else:
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


        telegram_userId = user_setting['Telegram']['userId']
        bot_token = user_setting['Telegram']['botToken']
        if user_setting['Telegram']['enable'] and len(telegram_userId) > 0 and len(bot_token) > 0:
            if bot_token in tgkeys:
                tgkeys[bot_token]['msg'] += user.msg
            else:
                tgkeys[bot_token] = {'msg': user.msg}

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

    for tgkey in tgkeys:
        push_url = 'https://api.telegram.org/bot' + tgkey + '/sendMessage'
        requests.post(push_url, data={
                      'chat_id': telegram_userId, 'text': tgkeys[tgkey]['msg']}, headers = {'Content-Type': 'application/x-www-form-urlencoded'})

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
    if user_count == 0:
        print('没有待运行的账号')
    return res


def setSongNumber():
    with open('./config.json', 'r', encoding='utf-8') as f:
        config = json5.load(f)
    setting = config['setting']
    lastSongNumber = os.environ.get("SONG_NUMBER", "-1")
    songNumber = ""
    timer_enable = False
    for user_config in config['users']:
        user_setting = setting
        if "setting" in user_config:
            for key in user_config['setting']:
                user_setting[key] = user_config['setting'][key]

        if user_setting['daka']['enable'] == False or user_setting['daka']['auto'] == False:
            continue

        user = User()
        user.setUser(username=user_config['username'], password=user_config['password'], countrycode=user_config.get(
            'countrycode', ''), user_setting=user_setting, No=0, ip=user_config['X-Real-IP'])
        if user.isLogined:
            resp = user.music.user_detail(user.uid)
            if user_setting['daka']['full_stop'] == True and (resp['level'] == 10 or resp['listenSongs'] >= 20000):
                continue
            songNumber += str(user.uid) + ":" + str(resp['listenSongs']) + ";"
            timer_enable = True
    if not timer_enable:
        # TODO
        pass
    if len(songNumber) == 0:
        songNumber = "-1"
    if lastSongNumber == "-1" and songNumber == "-1":
        return
    songNumber = time.strftime(
        "%Y-%m-%d", time.gmtime(time.time()+28800)) + "#" + songNumber

    Variables = []
    keylist = ["TENCENT_SECRET_ID", "TENCENT_SECRET_KEY"]
    for key in os.environ:
        if key == "SONG_NUMBER":
            Variables.append({"Key": "SONG_NUMBER", "Value": songNumber})
        elif key in keylist:
            Variables.append({"Key": key, "Value": os.environ.get(key)})

    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.scf.v20180416 import scf_client, models

    try:
        cred = credential.Credential(os.environ.get(
            "TENCENT_SECRET_ID"), os.environ.get("TENCENT_SECRET_KEY"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "scf.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, os.environ.get(
            "TENCENTCLOUD_REGION"), clientProfile)

        req = models.UpdateFunctionConfigurationRequest()
        params = {
            "FunctionName": os.environ.get("SCF_FUNCTIONNAME"),
            "Environment": {
                "Variables": Variables
            }
        }
        req.from_json_string(json.dumps(params))

        resp = client.UpdateFunctionConfiguration(req)
        print(resp.to_json_string())
        print("已更新歌曲播放数量")

    except TencentCloudSDKException as err:
        print(err)


def main_handler(event, context):
    if event.get("Type", "") == "Timer" and event.get("Message", "") == "set_song_number":
        setSongNumber()
        return
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
    start()
