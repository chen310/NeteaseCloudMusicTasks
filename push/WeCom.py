# -*- coding: utf-8 -*-
import requests
import json


def getKey(data):
    config = data['config']
    if len(config['corpid']) == 0 or len(config['agentid']) == 0 or len(config['secret']) == 0:
        return None
    return (config['module'], config['corpid'], config['agentid'], config['secret'], config['userid'], config['msgtype'])


def get_token(corpid, corpsecret):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {
        'corpid': corpid,
        'corpsecret': corpsecret,
    }
    req = requests.get(url, params=values)
    data = json.loads(req.text)
    if data["errcode"] == 0:
        return data["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(data))
        return None


def push(title, mdmsg, mdmsg_compat, textmsg, config):    
    msgtype = config['msgtype']
    if msgtype == 'markdown':
        msg = mdmsg
    else:
        msg = textmsg
    if len(config['corpid']) == 0 or len(config['agentid']) == 0 or len(config['secret']) == 0:
        return

    token = get_token(config['corpid'], config['secret'])
    if token is None:
        return
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token

    values = {
        "touser": config['userid'],
        "toparty": "",
        "totag": "",
        "msgtype": config['msgtype'],
        "agentid": config['agentid'],
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    if msgtype == "text":
        values["text"] = {"content": msg}
    elif msgtype == "textcard":
        values["textcard"] = {
            "title": title,
            "description": msg,
            "url": "URL",
            "btntxt": "详情"
        }
    elif msgtype == "markdown":
        values["markdown"] = {"content": msg}

    resp = requests.post(url, json=values)
    data = json.loads(resp.text)
    if data["errcode"] != 0:
        print("企业微信消息发送失败: "+str(data))
