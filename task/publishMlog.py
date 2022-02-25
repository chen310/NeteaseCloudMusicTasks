import random
import os
import time
import requests


def start(user, task={}):
    music = user.music

    if len(task['songId']) == 0:
        user.taskInfo(task['taskName'], '请填写歌曲ID')
        return

    songId = random.choice(task['songId'])
    song_resp = music.songs_detail([songId])
    if song_resp['code'] == 200 and len(song_resp['songs']) > 0:
        song = song_resp['songs'][0]
        songName = song['name']
        artists = song['ar']
        if artists is None or len(artists) == 0:
            artistName = '未知'
        else:
            artistName = '/'.join([a['name'] for a in artists])
        url = song.get('al', {}).get('picUrl', '')
    else:
        user.taskInfo(task['taskName'], '歌曲信息获取失败，请检查ID是否正确')

    if len(url) == 0:
        user.taskInfo(task['taskName'], '专辑图片获取失败')

    path = '/tmp'
    if not os.path.exists(path):
        path = './'

    filepath = os.path.join(path, 'album.jpg')
    size = task.get('size', 500)
    url += '?param='+str(size)+'y'+str(size)

    r = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(r.content)

    token = music.mlog_nos_token(filepath)
    time.sleep(0.2)
    music.upload_file(filepath, token)
    time.sleep(0.2)

    text = random.choice(task['text'])
    text = text.replace('$artist', artistName)
    text = text.replace('$song', songName)
    resp = music.mlog_pub(token, size, size, songId, songName, text)
    if resp['code'] != 200:
        user.taskInfo(task['taskName'], user.errMsg(resp))
        os.remove(filepath)
        return

    if task.get('delete', True) == True:
        time.sleep(0.5)
        resourceId = resp['data']['event']['info']['resourceId']
        delete_result = music.event_delete(resourceId)
        user.taskInfo(task['taskName'], '发布成功，已删除Mlog动态')
    else:
        user.taskInfo(task['taskName'], '发布成功')
    os.remove(filepath)
