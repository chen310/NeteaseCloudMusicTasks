# -*- coding: utf-8 -*-
import requests
import json


class WeComAlert():
    def __init__(self, corpid, corpsecret, agentid):
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid

    def get_token(self):
        url = self.url
        values = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret,
        }
        req = requests.get(url, params=values)
        data = json.loads(req.text)
        if data["errcode"] == 0:
            return data["access_token"]
        else:
            print("企业微信access_token获取失败: " + str(data))
            return None

    def send_msg(self, touser, msgtype, content, title="默认标题", user_url="URL"):
        token = self.get_token()
        if token is None:
            return
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token

        values = {
            "touser": touser,
            "toparty": "",
            "totag": "",
            "msgtype": msgtype,
            "agentid": self.agentid,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        if msgtype == "text":
            values["text"] = {"content": content}
        elif msgtype == "textcard":
            values["textcard"] = {
                "title": title,
                "description": content,
                "url": user_url,
                "btntxt": "详情"
            }
        elif msgtype == "markdown":
            values["markdown"] = {"content": content}

        resp = requests.post(url, json=values)
        data = json.loads(resp.text)
        if data["errcode"] != 0:
            print("企业微信消息发送失败: "+str(data))
