# -*- coding: utf-8 -*-
import requests
import json


def getKey(data):
    config = data['config']
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return None
    return (config['module'], config['userId'], config['botToken'])


def push(title, mdmsg, textmsg, config):
    msg = mdmsg
    if len(config['userId']) == 0 or len(config['botToken']) == 0:
        return

    url = 'https://api.telegram.org/bot' + config['botToken'] + '/sendMessage'
    requests.post(url, data={'chat_id': config['userId'], 'text': msg}, headers={
                  'Content-Type': 'application/x-www-form-urlencoded'})
