# -*- coding: utf-8 -*-
import requests
import json

def getKey(data):
    config = data['config']
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return None
    return (config['module'], config['userId'], config['botToken'])


def push(title, mdmsg, textmsg, config):
    msg = textmsg
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return
    server = config['server']
    if server:
        if server.endswith('/'):
            server = server[:-1]
    else:
        server = 'https://api.telegram.org'
    url = server +  '/bot' + config['botToken'] + '/sendMessage'
    ret = requests.post(url, data={'chat_id': config['userId'], 'text': msg}, headers={
                  'Content-Type': 'application/x-www-form-urlencoded'})
    print('Telegram response: \n', ret.status_code)
    if ret.status_code != 200:
        print(ret.content.decode('utf-8'))
