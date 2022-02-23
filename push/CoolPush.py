# -*- coding: utf-8 -*-
import requests


def getKey(data):
    config = data['config']
    if len(config['Skey']) == 0:
        return None
    return (config['module'], config['Skey'], config['method'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    msg = textmsg
    skey = config['Skey']
    method = config['method']
    if len(skey) == 0 or len(method) == 0:
        return

    CoolPush_url = "https://push.xuthus.cc/{}/{}".format(method, skey)
    if method == "email":
        requests.post(CoolPush_url, data={"t": title, "c": msg})
    else:
        requests.get(CoolPush_url, params={"c": msg})
