# -*- coding: utf-8 -*-
import requests
import json


def getKey(data):
    config = data['config']
    if len(config['pushToken']) == 0:
        return None
    return (config['module'], config['pushToken'], config['topic'], config['template'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    msg = mdmsg
    token = config['pushToken']
    topic = config['topic']
    template = config['template']
    if len(token) == 0:
        return

    url = 'http://www.pushplus.plus/send'

    data = {
        "token": token,
        "title": title,
        "content": msg
    }
    if len(topic) > 0:
        data['topic'] = topic
    if len(template) > 0:
        data['template'] = template

    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)
