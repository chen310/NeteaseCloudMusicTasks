import random


def start(user, task={}):
    music = user.music
    if len(task['name']) == 0:
        name = '歌单'
    else:
        name = random.choice(task['name'])
    create_resp = music.playlist_create(name, 0, 'SHARED')
    if create_resp['code'] == 200:
        if task['delete'] == True:
            music.playlist_delete(
                [create_resp.get('id', 0)])
            user.taskInfo(task['taskName'], '歌单创建成功，已删除')
        else:
            user.taskInfo(task['taskName'], '歌单创建成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(create_resp))
