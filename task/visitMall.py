def start(user, task={}):
    music = user.music

    resp = music.visit_mall()
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '访问成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
