# -*- coding: utf-8 -*-
import requests


def getKey(data):
    config = data['config']
    if len(config['KEY']) == 0:
        return None
    return (config['module'], config['KEY'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    msg = mdmsg
    key = config['KEY']
    if len(key) == 0:
        return

    if key.startswith('SCT'):
        url = 'https://sctapi.ftqq.com/' + key + '.send'
    else:
        url = 'https://sc.ftqq.com/' + key + '.send'

    requests.post(url, data={"text": title, "desp": msg})
