import random


def start(user, task={}):
    music = user.music

    if len(task['songId']) == 0:
        user.taskInfo(task['taskName'], '请填写歌曲id')
        return

    songId = random.choice(task['songId'])
    yunbeiNum = task['yunbeiNum']
    reason = random.choice(task['reason'])
    resp = music.yunbei_rcmd_submit(songId, yunbeiNum, reason)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '推歌成功，歌曲ID为'+str(songId))
    else:
        user.taskInfo(task['taskName'], '歌曲' + str(songId) + '推歌失败:' + user.errMsg(resp))
