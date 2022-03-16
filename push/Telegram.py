# -*- coding: utf-8 -*-
import requests
import json

def getKey(data):
    config = data['config']
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return None
    return (config['module'], config['userId'], config['botToken'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    #deprecate str.replace() funciton since Telegram support ** syntax to bold text.
    msg = mdmsg_compat # .replace('**', '*')
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return

    url = 'https://api.telegram.org/bot' + config['botToken'] + '/sendMessage'
    ret = requests.post(url, data={'chat_id': config['userId'], 'text': msg, 'parse_mode': "Markdown"}, headers={
                  'Content-Type': 'application/x-www-form-urlencoded'})
    print('Telegram response: \n', ret.status_code)
    if ret.status_code != 200:
        print(ret.content.decode('utf-8'))
