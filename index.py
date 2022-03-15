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
from utils import append_environ
import random


runtime = 'tencent-scf'


def md2text(data):
    data = re.sub(r'\n\n', r'\n', data)
    data = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1: \2 ', data)
    data = re.sub(r'\t', r'  ➢ ', data)
    data = re.sub(r'\*\*(.*?)\*\*\n', r'【\1】\n', data)
    data = re.sub(r'### ', r'\n', data)
    data = re.sub(r'`', r'', data)
    return data

def md2fullMd(data):
    data = re.sub(r'\*\*(.*?)\*\*\n', r'#### \1\n', data)
    data = re.sub(r'\t', r'- ', data)
    return data

def getSongNumber():
    res = {}
    if runtime == 'tencent-scf':
        if "SONG_NUMBER" in os.environ:
            sp1 = os.environ.get("SONG_NUMBER").split("#")
            if len(sp1) != 2:
                return res
            if sp1[0] != time.strftime("%Y-%m-%d", time.gmtime(time.time()+28800)):
                print("环境变量 SONG_NUMBER 已过期。是否未开启定时触发器 timer-songnumber")
                return res
            for number in sp1[1].split(";"):
                sp2 = number.split(":")
                if len(sp2) == 2:
                    res[sp2[0]] = int(sp2[1])
        else:
            print(
                "环境变量 SONG_NUMBER 不存在。项目地址: https://github.com/chen310/NeteaseCloudMusicTasks")
    return res


def start(event={}, context={}):
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json5.load(f)

    print('Version:', config['version'])

    # 公共配置
    setting = config['setting']

    songnumber = getSongNumber()
    # 推送
    pusher = Pusher()
    saved_environs = {}
    for user_config in config['users']:
        if not user_config['enable']:
            continue
        # 获取账号配置
        if "setting" in user_config:
            user_setting = updateConfig(user_config["setting"], setting)
        else:
            user_setting = setting

        user = User()
        user.runtime = runtime
        user.setUser(user_config, user_setting)
        if user.isLogined:
            user.songnumber = songnumber.get(str(user.uid), -1)
            user.startTask()

        for push in user_setting['push'].values():
            if not push['enable']:
                continue
            data = {
                'title': user.title,
                'mdmsg': md2fullMd(user.msg),
                'mdmsg_compat': user.msg,
                'textmsg': md2text(user.msg),
                'config': push
            }
            pusher.append(data)
        saved_environs.update(user.saved_environs)
    if len(saved_environs) > 0:
        res = append_environ(saved_environs)
        if res:
            print('已成功保存环境变量')
        else:
            print('环境变量保存失败')
    pusher.push()


def setSongNumber():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json5.load(f)
    setting = config['setting']
    lastSongNumber = os.environ.get("SONG_NUMBER", "-1")
    songNumber = ""
    timer_enable = False
    time.sleep(random.randint(10, 50))
    for user_config in config['users']:
        if not user_config['enable']:
            continue
        if "setting" in user_config:
            user_setting = updateConfig(user_config["setting"], setting)
        else:
            user_setting = setting

        if (not user_setting['daka']['enable']) or (not user_setting['daka']['auto']):
            continue

        user = User()
        user.runtime = runtime
        user.setUser(user_config, user_setting)
        if user.isLogined:
            if user.listenSongs == 0:
                resp = user.music.user_detail(user.uid)
                listenSongs = resp['listenSongs']
            else:
                listenSongs = user.listenSongs
            # if user_setting['daka']['full_stop'] == True and (resp['level'] == 10 or resp['listenSongs'] >= 20000):
            #     continue
            songNumber += str(user.uid) + ":" + str(listenSongs) + ";"
            timer_enable = True
        time.sleep(2)
    if not timer_enable:
        # TODO
        pass
    if len(songNumber) == 0:
        songNumber = "-1"
    if lastSongNumber == "-1" and songNumber == "-1":
        return
    songNumber = time.strftime(
        "%Y-%m-%d", time.gmtime(time.time()+28800)) + "#" + songNumber

    res = append_environ({"SONG_NUMBER": songNumber})
    if res:
        print("已更新歌曲播放数量")
    else:
        print("播放量更新失败")


def main_handler(event, context):
    if event.get("Type") == "Timer" and event.get("TriggerName") == "timer-songnumber":
        setSongNumber()
        return
    start(event, context)


if __name__ == '__main__':
    runtime = 'local'
    start()
