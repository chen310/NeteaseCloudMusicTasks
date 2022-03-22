import random


def start(user, task={}):
    music = user.music

    if len(task['id']) > 0:
        user_id = random.choice(task['id'])

        if len(task['msg']) > 0:
            msg = random.choice(task['msg'])
        else:
            msg = '你好'
        resp = music.msg_send(msg, [user_id])
        if resp['code'] == 200:
            user.taskInfo(task['taskName'], '发送成功')
        else:
            user.taskInfo(task['taskName'], user.errMsg(resp))
    else:
        user.taskInfo(task['taskName'], '请填写用户 ID')
