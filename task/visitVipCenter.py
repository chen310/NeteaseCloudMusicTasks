def start(user, task={}):
    music = user.music

    resp = music.vipcenter_task_external(1)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '浏览成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
