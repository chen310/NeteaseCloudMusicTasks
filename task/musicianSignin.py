def start(user, task={}):
    music = user.music

    resp = music.user_access()
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '签到成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
