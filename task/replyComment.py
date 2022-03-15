import random
import time
from . import publishComment


def start(user, task={}):
    music = user.music

    if len(user.comments) > 0:
        commentId = user.comments[0]['commentId']
        songId = user.comments[0]['songId']
    else:
        if len(task['id']) > 0:
            # 发布主创说
            publishComment.start(user, user.user_setting['musician_task']['755000'])
        else:
            return
    time.sleep(5)
    if len(user.comments) > 0:
        commentId = user.comments[0]['commentId']
        songId = user.comments[0]['songId']
    else:
        return user.taskInfo(task['taskName'] + '-发布评论', '发布失败')

    if len(task['msg']) > 0:
        msg = random.choice(task['msg'])
    else:
        msg = '感谢收听'
    resp = music.comments_reply(
        songId, commentId, msg)
    if resp['code'] == 200:
        user.replies.append(
            {'commentId': resp['comment']['commentId'], 'songId': songId})
        user.taskInfo(task['taskName'], '回复成功')
    else:
        user.taskInfo(task['taskName'] + '-回复评论', user.errMsg(resp))
