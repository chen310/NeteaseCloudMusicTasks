import time
import re

def start(user, task={}):
    music = user.music

    progress = music.signin_progress('1207signin-1207signin')
    if progress['code'] != 200:
        print('签到进度获取失败', user.errMsg(progress))
        music.daily_task()
        return

    if progress['data']['today']['todaySignedIn']:
        stats = progress['data']['today']['todayStats']
        totalYunbei = 0
        for stat in stats:
            currentProgress = stat['currentProgress']
            for prize in stat['prizes']:
                if prize['obtained'] == True and prize['progress'] == currentProgress:
                    totalYunbei += prize['amount']
        user.taskInfo('重复签到', '今天签到共获取' + str(totalYunbei) + '云贝')

    music.daily_task()
    time.sleep(1)
    progress = music.signin_progress('1207signin-1207signin')
    if not progress['data']['today']['todaySignedIn']:
        user.taskInfo('无法确定是否签到成功，请稍后到云贝中心检查云贝是否到账')

    stats = progress['data']['today']['todayStats']
    for stat in stats:
        desp = stat['description']
        desp = re.sub(r'（.*?）', '', desp)
        desp = re.sub(r'\(.*?\)', '', desp)
        currentProgress = stat['currentProgress']
        for prize in stat['prizes']:
            if prize['obtained'] == True and prize['progress'] == currentProgress:
                user.taskInfo(desp, '云贝+' + str(prize['amount']) + ' 已签到'+str(currentProgress)+'天')
