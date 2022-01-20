# -*- coding: utf-8 -*-
from utils import updateConfig
import time
import requests
import json
import json5
import re
import os
from user import User
from pusher import Pusher


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
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json5.load(f)

    # 公共配置
    setting = config['setting']

    songnumber = getSongNumber()
    # 推送
    pusher = Pusher()
    for user_config in config['users']:
        if not user_config['enable']:
            continue
        # 获取账号配置
        if "setting" in user_config:
            user_setting = updateConfig(user_config["setting"], setting)
        else:
            user_setting = setting

        user = User()
        user.setUser(user_config, user_setting)
        if user.isLogined:
            user.songnumber = songnumber.get(str(user.uid), -1)
            user.startTask()

        for push in user_setting['push'].values():
            if not push['enable']:
                continue
            data = {
                'title': user.title,
                'mdmsg': user.msg,
                'textmsg': md2text(user.msg),
                'config': push
            }
            pusher.append(data)
    pusher.push()


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
        user.setUser(user_config, user_setting)
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
    if event.get("Type") == "Timer" and event.get("TriggerName") == "timer-songnumber":
        setSongNumber()
        return
    start(event, context)


if __name__ == '__main__':
    start()
