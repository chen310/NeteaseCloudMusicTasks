# -*- coding: utf-8 -*-
import time
import random
import math
import re
from api import NetEase
import os
import requests


class User(object):
    def __init__(self):
        self.music = None
        self.user_setting = {}
        self.title = '网易云音乐'
        self.msg = ''
        self.isLogined = False
        self.nickname = ''
        self.uid = 0
        self.artistId = 0
        self.userType = 0
        self.level = 0
        self.full = False
        self.songFull = False
        self.listenSongs = 0
        self.vipType = 0
        self.songnumber = -1
        self.runtime = ''

        self.comments = []
        self.replies = []
        self.saved_environs = {}

    def errMsg(self, data):
        if 'msg' in data and data['msg'] is not None:
            return str(data['code']) + ':' + data['msg']
        elif 'message' in data and data['message'] is not None:
            return str(data['code']) + ':' + data['message']
        else:
            return str(data)

    def setUser(self, user_config, user_setting):
        if len(user_config['username']) == 0 and len(user_config['cookie']) == 0:
            self.title += ': 请填写账号密码或cookie'
            self.taskTitle('用户信息')
            self.taskInfo('登录失败，请填写账号密码或cookie')
            raise Exception('请填写账号密码或cookie')
        self.music = self.login_check(user_config['username'], user_config['password'], user_config['cookie'], user_config.get(
            'countrycode', ''), user_config['X-Real-IP'])
        if self.music.uid != 0:
            self.isLogined = True
            self.user_setting = user_setting
            self.uid = self.music.uid
            self.userType = self.music.userType
        else:
            if len(self.music.loginerror) > 0:
                msg = self.music.loginerror
            else:
                msg = '可能是网络或其他原因'
            self.title += ': 登录失败'
            self.taskTitle('用户信息')
            self.taskInfo('登录失败，' + msg)
            self.finishTask()
    def set_cookies(self, cookie, music):
        cookies = {}
        sp = cookie.split(";")
        cookies = {}
        for c in sp:
            t = []
            if ':' in c:
                t = c.split(':')
            elif '=' in c:
                t = c.split('=')
            if len(t) == 2:
                cookies[t[0]] = t[1]
        if len(cookies) > 0:
            cookies['__remember_me'] = 'true'
            for key, value in cookies.items():
                c = music.make_cookie(key, value)
                music.session.cookies.set_cookie(c)

    def login_check(self, username, pwd='', cookie='', countrycode='', ip=''):
        music = NetEase(username)
        if len(ip) > 0:
            music.header["X-Real-IP"] = ip

        if len(cookie) > 0:
            self.set_cookies(cookie, music)
            resp = music.user_level()
            if resp['code'] == 200:
                print('已通过配置文件中的 cookie 登录')
                music.uid = resp['data']['userId']
                user_resp = music.user_detail(music.uid)
                if 'artistId' in user_resp['profile']:
                    self.artistId = user_resp['profile']['artistId']
                self.listenSongs = user_resp['listenSongs']
                music.nickname = user_resp['profile']['nickname']
                music.userType = user_resp['profile']['userType']
                if music.userType != 0 and music.userType != 4:
                    for authtype in user_resp['profile'].get('allAuthTypes', []):
                        if authtype['type'] == 4:
                            music.userType = 4
                            break
                return music
            else:
                print('配置文件中的 cookie 填写错误或已失效')
                music.session.cookies.clear()

        if self.runtime == 'tencent-scf':
            var_name = 'COOKIE_' + re.sub('[^a-zA-Z0-9]', '_', username)
            if var_name in os.environ:
                self.set_cookies(os.environ.get(var_name), music)
        resp = music.user_level()
        if resp['code'] == 200:
            print('已通过 cookie 登录')
            music.uid = resp['data']['userId']
            user_resp = music.user_detail(music.uid)
            if 'artistId' in user_resp['profile']:
                self.artistId = user_resp['profile']['artistId']
            self.listenSongs = user_resp['listenSongs']
            music.nickname = user_resp['profile']['nickname']
            music.userType = user_resp['profile']['userType']
            if music.userType != 0 and music.userType != 4:
                for authtype in user_resp['profile'].get('allAuthTypes', []):
                    if authtype['type'] == 4:
                        music.userType = 4
                        break
        else:
            if len(pwd) == 0:
                music.uid = 0
                music.nickname = ''
                music.loginerror = '请填写账号密码'
                return music
            login_resp = music.login(username, pwd, countrycode)
            if login_resp['code'] == 200:
                time.sleep(3)
                level_resp = music.user_level()
                if level_resp['code'] == 301:
                    music.loginerror = str(login_resp['profile']['userId']) + ' 运行失败，请尝试删除云函数后重新部署'
                    music.uid = 0
                    return music
                print('已通过账号密码登录')                
                if self.runtime == 'tencent-scf':
                    music_cookie = ''
                    for cookie in music.session.cookies:
                        if cookie.name == 'MUSIC_U':
                            music_cookie += 'MUSIC_U:' + cookie.value + ';'
                        elif cookie.name == '__csrf':
                            music_cookie += '__csrf:' + cookie.value + ';'

                    self.saved_environs['COOKIE_' + re.sub('[^a-zA-Z0-9]', '_', username)] = music_cookie

                music.uid = login_resp['profile']['userId']
                music.nickname = login_resp['profile']['nickname']
                music.userType = login_resp['profile']['userType']
                if 'artistId' in login_resp['profile']:
                    self.artistId = login_resp['profile']['artistId']
                music.loginerror = ''
                if music.userType != 0 and music.userType != 4:
                    user_resp = music.user_detail(music.uid)
                    for authtype in user_resp['profile'].get('allAuthTypes', []):
                        if authtype['type'] == 4:
                            music.userType = 4
                            break
            else:
                music.uid = 0
                music.nickname = ''
                if login_resp['code'] == -1:
                    music.loginerror = ''
                elif login_resp['code'] == -462:
                    music.loginerror = '暂时无法通过账号密码登录，请在配置文件中填写 cookie 进行登录'
                else:
                    music.loginerror = login_resp.get('msg', str(login_resp))

        return music

    def taskTitle(self, title):
        msg = '**{}**\n'.format(title)
        self.msg += msg + '\n'
        print(msg)
    def taskInfo(self, key, value='', useCodeblock = True):
        if value == '':
            msg = f"\t{str(key)}"
        elif useCodeblock:
            # Use `codeblock` to prevent markdown 's keywords containing in value which leads to 400 Bad Request
            msg = f"\t{str(key)}: `{str(value)}`"
        else:
            msg = f"\t{str(key)}: {str(value)}"
        self.msg += msg + '\n'
        print(msg)


    def finishTask(self):
        self.msg += '\n'
        print()

    def userInfo(self):
        resp = self.music.user_detail(self.uid)
        if 'artistId' in resp['profile']:
            self.artistId = resp['profile']['artistId']
        self.level = resp['level']
        self.vipType = resp['profile']['vipType']
        self.listenSongs = resp['listenSongs']
        self.taskTitle('用户信息')
        self.taskInfo('用户名称', resp['profile']['nickname'])
        self.taskInfo('用户ID', self.uid)
        self.taskInfo('用户等级', resp['level'])
        self.taskInfo('用户村龄', str(resp['createDays']) + '天')

        if self.vipType == 11:
            vip_resp = self.music.vip_level()
            self.taskInfo('VIP等级', vip_resp['data']['redVipLevel'])
            self.taskInfo('到期时间', time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(vip_resp['data']['musicPackage']['expireTime']/1000)))

        self.taskInfo('云贝数量', resp['userPoint']['balance'])

        attention_resp = self.music.expire_attention()
        if attention_resp['code'] == 200 and attention_resp['data']['expiringYunbei'] > 0:
            remainingTime = attention_resp['data']['remainingTime']
            self.taskInfo('过期提醒', str(
                attention_resp['data']['expiringYunbei']) + '云贝将在' + str(remainingTime)+'天后过期，请尽快使用')

        self.taskInfo('粉丝数量', resp['profile']['followeds'])
        self.taskInfo('听歌总数', self.listenSongs)
        self.taskInfo('歌单数', resp['profile']['playlistCount'])
        self.taskInfo('歌单总收藏数', resp['profile']['playlistBeSubscribedCount'])

        resp = self.music.user_level()
        self.full = resp['full']
        if not self.full:
            self.taskInfo('距离下级还需播放', str(
                resp['data']['nextPlayCount'] - resp['data']['nowPlayCount']) + '首歌')
            self.taskInfo('距离下级还需登录', str(
                resp['data']['nextLoginCount'] - resp['data']['nowLoginCount']) + '天')
            if resp['data']['nowPlayCount'] >= 20000:
                self.songFull = True
        self.finishTask()

    def resize(self, total):
        if total <= 10:
            total = total * 3
        elif total <= 50:
            total = int(total * 1.8)
        elif total <= 100:
            total = int(total * 1.3)
        elif total <= 200:
            total = int(total * 1.2)
        return total

    def auto_daka(self):
        self.taskTitle('打卡信息')
        user_setting = self.user_setting

        if user_setting['daka']['full_stop']:
            if self.full:
                self.taskInfo('打卡', '您的等级已经爆表了，无需再打卡')
                self.finishTask()
                return
            elif self.songFull:
                self.taskInfo('打卡', '距离满级只差登录天数，无需打卡')
                self.finishTask()
                return
        print("获取到歌曲数:" + str(self.songnumber))
        daka_number = 0

        total = 300 - (self.listenSongs - self.songnumber)
        if total == 0:
            self.taskInfo('打卡', '今天300首歌已经刷满了')
            self.finishTask()
            return
        if total <= user_setting['daka']['tolerance']:
            self.taskInfo('打卡', '今天已经打卡' +
                          str(self.listenSongs - self.songnumber)+"首歌了")
            self.finishTask()
            return
        playlists = self.music.personalized_playlist(limit=50)
        # 推荐歌单id列表
        playlist_ids = [playlist["id"] for playlist in playlists]
        song_ids = []

        song_datas = []
        # 打乱歌单id
        random.shuffle(playlist_ids)
        idx = 0
        start = idx
        total = self.resize(total)
        for c in range(6):
            if len(song_datas) < total:
                for i in range(start, len(playlist_ids)):
                    idx = i
                    playlist_id = playlist_ids[i]
                    # 获得歌单中歌曲的信息
                    songs = self.music.playlist_detail(playlist_id).get(
                        "playlist", {}).get("tracks", [])
                    for song in songs:
                        # 去重
                        if song['id'] in song_ids:
                            break
                        song_ids.append(song["id"])
                        song_data = {
                            "type": 'song',
                            "wifi": 0,
                            "download": 0,
                            "id": song['id'],
                            "time": math.ceil(song['dt']/1000),
                            "end": 'playend',
                            "source": 'list',
                            "sourceId": playlist_id,
                        }
                        song_datas.append(song_data)
                    if len(song_datas) >= total:
                        song_datas = song_datas[0:total]
                        break
            num = 300
            print("即将打卡"+str(total)+"首")
            self.music.daka(song_datas[0:total])
            daka_number += total
            song_datas = song_datas[total:]
            # time.sleep(user_setting['daka']['sleep_time'])
            time.sleep(30)
            resp = self.music.user_detail(self.uid)
            if 300 - (resp['listenSongs'] - self.songnumber) <= user_setting['daka']['tolerance']:
                self.title = self.title + '今天听歌' + \
                    str(resp['listenSongs']-self.songnumber) + \
                    '首，累计听歌'+str(resp['listenSongs'])+'首'
                self.taskInfo("本次实际打卡数", str(daka_number) + '首')
                self.taskInfo('今天有效打卡数', str(
                    resp['listenSongs'] - self.songnumber) + '首')
                self.taskInfo('听歌总数', str(resp['listenSongs']) + '首')
                if resp['listenSongs'] - self.songnumber < 300:
                    self.taskInfo(
                        '温馨提示', '数据更新可能有延时，[点击查看最新数据](https://music.163.com/#/user/home?id='+str(self.uid)+')', useCodeblock=False)
                return
            else:
                total = 300 - (resp['listenSongs'] - self.songnumber)
                total = self.resize(total)
                if len(song_datas) >= total:
                    start = idx
                else:
                    start = idx + 1

        time.sleep(15)
        resp = self.music.user_detail(self.uid)
        self.title = self.title + '今天听歌' + \
            str(resp['listenSongs']-self.songnumber) + \
            '首，累计听歌'+str(resp['listenSongs'])+'首'
        self.taskInfo("本次实际打卡数", str(daka_number) + '首')
        self.taskInfo('今天有效打卡数', str(
            resp['listenSongs'] - self.songnumber) + '首')
        self.taskInfo('听歌总数', str(resp['listenSongs']) + '首')
        if resp['listenSongs'] - self.songnumber < 300:
            self.taskInfo(
                '温馨提示', '数据更新可能有延时，[点击查看最新数据](https://music.163.com/#/user/home?id='+str(self.uid)+')', useCodeblock=False)
        self.finishTask()

    def daka(self):
        self.taskTitle('打卡信息')
        user_setting = self.user_setting

        if user_setting['daka']['full_stop']:
            if self.full:
                self.taskInfo('打卡', '您的等级已经爆表了，无需再打卡')
                self.finishTask()
                return
            elif self.songFull:
                self.taskInfo('打卡', '距离满级只差登录天数，无需打卡')
                self.finishTask()
                return

        playlists = self.music.personalized_playlist(limit=30)
        # 推荐歌单id列表
        playlist_ids = [playlist["id"] for playlist in playlists]
        song_ids = []

        total = user_setting['daka']['song_number']
        song_datas = []
        # 打乱歌单id
        random.shuffle(playlist_ids)
        for playlist_id in playlist_ids:
            # 获得歌单中歌曲的信息
            songs = self.music.playlist_detail(playlist_id).get(
                "playlist", {}).get("tracks", [])
            for song in songs:
                # 去重
                if song['id'] in song_ids:
                    break
                song_ids.append(song["id"])
                song_data = {
                    "type": 'song',
                    "wifi": 0,
                    "download": 0,
                    "id": song['id'],
                    "time": math.ceil(song['dt']/1000),
                    "end": 'playend',
                    "source": 'list',
                    "sourceId": playlist_id,
                }
                song_datas.append(song_data)
            if len(song_datas) >= total:
                song_datas = song_datas[0:total]
                break

        num = user_setting['daka']['upload_num']
        for i in range(0, len(song_datas), num):
            self.music.daka(song_datas[i:i+num])
            time.sleep(user_setting['daka']['sleep_time'])
            resp = self.music.user_detail(self.uid)
            if (resp['listenSongs'] - self.listenSongs) >= 300:
                self.title = self.title + '本次听歌' + \
                    str(resp['listenSongs']-self.listenSongs) + \
                    '首，累计听歌'+str(resp['listenSongs'])+'首'
                self.taskInfo('本次打卡数', str(
                    resp['listenSongs'] - self.listenSongs) + '首')
                self.taskInfo('听歌总数', str(resp['listenSongs']) + '首')
                if resp['listenSongs'] - self.listenSongs < 300:
                    self.taskInfo(
                        '温馨提示', '数据更新可能有延时，[点击查看最新数据](https://music.163.com/#/user/home?id='+str(self.uid)+')', useCodeblock=False)
                return

        time.sleep(user_setting['daka']['sleep_time'] + 5)
        resp = self.music.user_detail(self.uid)
        self.title = self.title + '本次听歌' + \
            str(resp['listenSongs']-self.listenSongs) + \
            '首，累计听歌'+str(resp['listenSongs'])+'首'
        self.taskInfo('本次打卡数', str(
            resp['listenSongs'] - self.listenSongs) + '首')
        self.taskInfo('听歌总数', str(resp['listenSongs']) + '首')
        if resp['listenSongs'] - self.listenSongs < 300:
            self.taskInfo(
                '温馨提示', '数据更新可能有延时，[点击查看最新数据](https://music.163.com/#/user/home?id='+str(self.uid)+')', useCodeblock=False)
        self.finishTask()

    def play_playlists(self):
        user_setting = self.user_setting
        self.taskTitle('播放歌单')
        playlist_ids = user_setting['other']['play_playlists']['playlist_ids']
        if len(playlist_ids) == 0:
            self.taskInfo('无可播放歌单')
            return
        count = user_setting['other']['play_playlists']['times']

        song_datas = []
        for playlist_id in playlist_ids:
            # 获得歌单中歌曲的信息
            result = self.music.playlist_detail(playlist_id)
            if result['code'] != 200:
                self.taskInfo('歌单' + str(playlist_id), self.errMsg(result))
                break
            songs = result.get("playlist", {}).get("tracks", [])
            self.taskInfo(result["playlist"]['name'], '播放' + str(count) + '次')

            for song in songs:
                song_data = {
                    "type": 'song',
                    "wifi": 0,
                    "download": 0,
                    "id": song['id'],
                    "time": math.ceil(song['dt']/1000),
                    "end": 'playend',
                    "source": 'list',
                    "sourceId": playlist_id,
                }
                song_datas.append(song_data)
        for i in range(count):
            for playlist_id in playlist_ids:
                self.music.update_playcount(playlist_id)
            self.play(song_datas)
            time.sleep(1)

        self.finishTask()

    def yunbei_task(self):
        user_setting = self.user_setting

        self.taskTitle('云贝任务')
        count = 0
        resp = self.music.yunbei_task()
        tasks = user_setting['yunbei_task']
        for t in resp['data']:
            taskId = str(t['taskId'])
            if t['userTaskId'] == 0 and taskId in tasks and tasks[taskId]['enable']:
                exec('from task import {}'.format(tasks[taskId]['module']))
                exec('{}.start(self, tasks[taskId])'.format(
                    tasks[taskId]['module']))
                count += 1

        if count == 0:
            self.taskInfo('无可执行的任务')

        self.finishTask()
        time.sleep(1)

    def get_yunbei(self):
        self.taskTitle('领取云贝')
        resp = self.music.yunbei_task_todo()
        count = 0
        for task in resp['data']:
            if task['userTaskId'] > 0:
                self.music.yunbei_task_finish(
                    task['userTaskId'], task['depositCode'])
                self.taskInfo(task['taskName'], '云贝+' + str(task['taskPoint']))
                count += 1
        if count == 0:
            self.taskInfo('无可领取的云贝')

        self.finishTask()

    def play(self, song_datas, sleep_time=3):
        if "upload_num" in self.user_setting['daka']:
            num = self.user_setting['daka']['upload_num']
        else:
            num = 300
        for i in range(0, len(song_datas), num):
            self.music.daka(song_datas[i:i+num])
            time.sleep(sleep_time)

    def follow(self):
        # 转载注明来源: https://github.com/chen310/NeteaseCloudMusicTasks
        # 勿修改作者 ID
        author_uid = 347837981
        if self.uid == author_uid:
            return
        resp = self.music.user_detail(author_uid)
        author_nickname = resp['profile']['nickname']
        if not resp['profile']['followed']:
            follow_resp = self.music.user_follow(author_uid)
            if follow_resp['code'] == 200:
                self.taskTitle('关注作者')
                self.taskInfo('感谢关注', author_nickname)
                # self.taskInfo('如果不想关注，请在配置文件里修改，并在官方客户端里取消关注')
                self.taskInfo(
                    '如果不想关注，请在配置文件里修改，并在[主页](https://music.163.com/#/user/home?id='+str(author_uid)+')里取消关注', useCodeblock=False)
                self.finishTask()

    def sign(self):
        self.taskTitle('签到信息')

        progress = self.music.signin_progress('1207signin-1207signin')
        if progress['code'] != 200:
            print('签到进度获取失败', self.errMsg(progress))
            self.music.daily_task()
            self.taskInfo('签到成功')
            self.finishTask()
            return

        if progress['data']['today']['todaySignedIn'] == True:
            stats = progress['data']['today']['todayStats']
            totalYunbei = 0
            for stat in stats:
                currentProgress = stat['currentProgress']
                for prize in stat['prizes']:
                    if prize['obtained'] == True and prize['progress'] == currentProgress:
                        totalYunbei += prize['amount']
            self.taskInfo('重复签到', '今天签到共获取' + str(totalYunbei) + '云贝')
            self.finishTask()
            return

        self.music.daily_task()
        time.sleep(1)
        progress = self.music.signin_progress('1207signin-1207signin')
        if progress['data']['today']['todaySignedIn'] == False:
            self.taskInfo('无法确定是否签到成功，请稍后到云贝中心检查云贝是否到账')
            self.finishTask()
            return

        stats = progress['data']['today']['todayStats']
        for stat in stats:
            desp = stat['description']
            desp = re.sub(r'（.*?）', '', desp)
            desp = re.sub(r'\(.*?\)', '', desp)
            currentProgress = stat['currentProgress']
            for prize in stat['prizes']:
                if prize['obtained'] == True and prize['progress'] == currentProgress:
                    self.taskInfo(
                        desp, '云贝+' + str(prize['amount']) + ' 已签到'+str(currentProgress)+'天')
        self.finishTask()

    def get_missions(self):
        cycle_result = self.music.mission_cycle_get()
        time.sleep(0.5)
        stage_result = self.music.mission_stage_get()

        missions = []
        if cycle_result['code'] == 200:
            missions.extend(cycle_result.get('data', {}).get('list', []))
        if stage_result['code'] == 200:
            for mission in stage_result['data']['list']:
                for target in  mission['userStageTargetList']:
                    m = mission.copy()
                    m['status'] = target['status']
                    m['progressRate'] = target['progressRate']
                    m['targetCount'] = target['sumTarget']
                    m['rewardWorth'] = target['worth']
                    if 'userMissionId' in target:
                        m['userMissionId'] = target['userMissionId']
                    missions.append(m)

        return missions

    def musician_task(self):
        self.taskTitle('音乐人信息')

        tasks = self.user_setting["musician_task"]

        mission_list = self.get_missions()

        if len(mission_list) > 0:
            for mission in mission_list:
                missionId = str(mission['missionId'])
                status = mission['status']
                if (status == 0 or status == 10) and missionId in tasks and tasks[missionId]['enable']:
                    exec('from task import {}'.format(
                        tasks[missionId]['module']))
                    exec('{}.start(self, tasks[missionId])'.format(
                        tasks[missionId]['module']))

            if tasks['732004']['delete'] and len(self.replies) > 0:
                for reply in self.replies:
                    resp = self.music.comments_delete(
                        reply['songId'], reply['commentId'])
                    if resp['code'] == 200:
                        print('评论删除成功')
                    else:
                        print('评论删除失败')
            if tasks['755000']['delete'] and len(self.comments) > 0:
                for comment in self.comments:
                    resp = self.music.comments_delete(
                        comment['songId'], comment['commentId'])
                    if resp['code'] == 200:
                        print('回复删除成功')
                    else:
                        print('回复删除失败')

        time.sleep(7)
        mission_list = self.get_missions()
        if len(mission_list) > 0:        
            for mission in mission_list:
                missionId = str(mission['missionId'])
                if mission['status'] == 0 and missionId in tasks:
                    if tasks[missionId]['enable']:
                        self.taskInfo(mission['description'], '未完成')
                    else:
                        self.taskInfo(mission['description'], '未开启任务')
                elif mission['status'] == 10:
                    self.taskInfo(mission['description'], '进行中' + '(' + str(
                        mission['progressRate']) + '/' + str(mission['targetCount']) + ')')
                elif mission['status'] == 20:
                    description = mission['description']
                    userMissionId = mission['userMissionId']
                    period = mission['period']
                    rewardWorth = mission['rewardWorth']

                    if 'userStageTargetList' in mission:
                        self.taskInfo(description, '任务已完成')
                        continue

                    reward_result = self.music.reward_obtain(
                        userMissionId=userMissionId, period=period)
                    if reward_result['code'] == 200:
                        self.taskInfo(description, '云豆+' + str(rewardWorth))
                    else:
                        self.taskInfo(description, '云豆领取失败:' +
                                      self.errMsg(reward_result))
                elif mission['status'] == 100 and missionId in tasks:
                    self.taskInfo(mission['description'], '云豆已经领取过了')
        else:
            self.taskInfo('任务获取失败')

        bean_resp = self.music.cloudbean()
        self.taskInfo('云豆数', bean_resp['data']['cloudBean'])

        info_result = self.music.musician_data()
        data = info_result.get('data')

        if data is None:
            self.finishTask()
            return

        if data.get('playCount') is None:
            self.taskInfo('昨日播放量', '--')
        else:
            self.taskInfo('昨日播放量', data['playCount'])

        if data.get('followerCountIncrement') is None:
            self.taskInfo('昨日新增粉丝', '--')
        else:
            self.taskInfo('昨日新增粉丝', data['followerCountIncrement'])

        if data.get('productionTotal') is None:
            self.taskInfo('作品(首)', '--')
        else:
            self.taskInfo('作品(首)', data['productionTotal'])

        if data.get('availableExtractIncomeTotal') is None:
            self.taskInfo('可提现余额', '--')
        else:
            self.taskInfo('可提现余额', data['availableExtractIncomeTotal'])

        if data.get('musicianLevelScore') is None:
            self.taskInfo('音乐人指数', '--')
        else:
            self.taskInfo('音乐人指数', data['musicianLevelScore'])

        self.finishTask()

    def vip_task(self):
        self.taskTitle('VIP成长值')

        resp = self.music.vip_task_newlist()
        items = []
        tasks = self.user_setting["vip_task"]
        taskLists = resp.get('data', {}).get('taskList', [])
        for taskList in taskLists:
            for task_items in taskList.get('taskItems', []):
                item = task_items.get('currentInfo', None)
                if (item is not None):
                    items.append(item)
                subitems = task_items.get('subList', [])
                if (subitems is not None):
                    for item in subitems:
                        if (item is not None):
                            items.append(item)
        count = 0
        for item in items:
            desp = item['action']
            actionType = str(item['actionType'])
            if item['status'] == 0 and actionType in tasks and tasks[actionType]['enable']:
                exec('from task import {}'.format(tasks[actionType]['module']))
                exec('{}.start(self, tasks[actionType])'.format(
                    tasks[actionType]['module']))
                count += 1

        if count > 0:
            time.sleep(3)
            resp = self.music.vip_task_newlist()
        else:
            self.taskInfo('无可执行的任务')

        unGetAllScore = resp.get('data', {}).get('unGetAllScore', 0)

        if unGetAllScore == 0:
            self.taskInfo('没有可领取的成长值')
            self.finishTask()
            return

        reward_resp = self.music.vip_reward_getall()
        if reward_resp['code'] != 200:
            self.taskInfo('成长值领取失败', self.errMsg(reward_resp))
            self.finishTask()
            return

        scores = 0

        taskLists = resp.get('data', {}).get('taskList', [])
        for taskList in taskLists:
            for items in taskList.get('taskItems', []):
                item = items.get('currentInfo', None)
                if (item is not None):
                    desp = item['action']
                    if item['totalUngetScore'] > 0:
                        scores += item['totalUngetScore']
                        self.taskInfo(
                            desp, '成长值+' + str(item['totalUngetScore']))

                items = items.get('subList', [])
                if (items is not None):
                    for item in items:
                        desp = item['action']
                        if item['totalUngetScore'] > 0:
                            scores += item['totalUngetScore']
                            self.taskInfo(
                                desp, '成长值+' + str(item['totalUngetScore']))

        if unGetAllScore > scores:
            self.taskInfo('未知', '成长值+' + str(unGetAllScore - scores))
        self.finishTask()

    def startTask(self):
        self.userInfo()

        if self.user_setting['follow']:
            self.follow()

        if self.user_setting['sign']:
            self.sign()

        self.yunbei_task()
        time.sleep(3)
        self.get_yunbei()

        if self.userType == 4:
            time.sleep(3)
            self.musician_task()

        if self.vipType == 11:
            self.vip_task()

        if self.user_setting['daka']['enable']:
            if self.user_setting['daka']['auto'] == True and self.songnumber != -1:
                self.auto_daka()
            else:
                self.daka()

        if self.user_setting['other']['play_playlists']['enable']:
            self.play_playlists()
