import random


def start(user, task={}):
    music = user.music

    if len(task['id']) > 0 and len(user.comments) == 0:
        songId = random.choice(task['id'])
        if len(task['msg']) > 0:
            msg = random.choice(task['msg'])
        else:
            msg = '感谢大家收听'

        resp = music.comments_add(songId, msg)
        if resp['code'] == 200:
            user.comments.append(
                {'commentId': resp['comment']['commentId'], 'songId': songId})
            user.taskInfo(task['taskName'], '发布成功')
        else:
            user.taskInfo(task['taskName'], user.errMsg(resp))
