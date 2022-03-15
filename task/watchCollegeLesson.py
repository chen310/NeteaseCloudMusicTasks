def start(user, task={}):
    music = user.music

    resp = music.watch_college_lesson()
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '观看成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
