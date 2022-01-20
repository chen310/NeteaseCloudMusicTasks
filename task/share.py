


def start(user, task={}):
    music = user.music

    resp = music.daily_task(3)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '分享成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
