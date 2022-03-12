def start(user, task={}):
    music = user.music

    resourceId = ''
    if 'circleId' in task and len(task['circleId']) > 0:
        resourceId = task['circleId']
    else:
        artistId = user.artistId
        if not artistId:
            user.taskInfo(task['taskName'], 'artistId 获取失败')
            return
        artist_resp = music.artist_homepage(artistId)
        blocks = artist_resp['data']['blocks']
        for block in blocks:
            if block['showType'] == 'MY_CIRCLE_WITH_MORE':
                creatives = block['creatives']
                for creative in creatives:
                    resources = creative['resources']
                    for resource in resources:
                        if resource['resourceType'] == 'CIRCLE':
                            resourceId = resource['resourceId']
                            break
                    if resourceId:
                        break
            if resourceId:
                break
    if not resourceId:
        user.taskInfo(task['taskName'], 'resourceId 获取失败')
        return
    resp = music.circle_get(resourceId)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '访问成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
