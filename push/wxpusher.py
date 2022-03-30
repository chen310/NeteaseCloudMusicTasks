import requests


def getKey(data):
    config = data['config']
    if len(config['APP_TOKEN']) == 0 or len(config['UID']) == 0:
        return None
    return (config['module'], config['APP_TOKEN'], config['UID'])


def push(title, mdmsg, textmsg, config):
    data = {
        "appToken": config['APP_TOKEN'],
        "content": mdmsg,
        "summary": title,
        "contentType": 3,
        "topicIds": [],
        "uids": [config['UID']]
    }
    url = "http://wxpusher.zjiecode.com/api/send/message"
    requests.post(url, json=data)
