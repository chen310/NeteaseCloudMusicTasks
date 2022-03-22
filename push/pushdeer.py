import json
from typing import Optional, Union
import requests


def getKey(data):
    config = data['config']
    if len(config['pushkey']) == 0:
        return None
    return (config['module'], config['pushkey'], config['server'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    msg = mdmsg
    pushkey = config['pushkey']
    if len(pushkey) == 0:
        return
    if config['server']:
        pushdeer = PushDeer(server=config['server'], pushkey=pushkey)
    else:
        pushdeer = PushDeer(pushkey=pushkey)
    pushdeer.send_markdown(title, desp=msg)

# From https://github.com/gaoliang/pypushdeer
class PushDeer:
    server = "https://api2.pushdeer.com"
    endpoint = "/message/push"
    pushkey = None

    def __init__(self, server: Optional[str] = None, pushkey: Optional[str] = None):
        if server:
            self.server = server
        if pushkey:
            self.pushkey = pushkey

    def _push(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
              pushkey: Optional[str] = None, text_type: Optional[str] = None):

        if not pushkey and not self.pushkey:
            raise ValueError("pushkey must be specified")

        res = self._send_push_request(desp, pushkey or self.pushkey, server or self.server, text, text_type)
        if res["content"]["result"]:
            result = json.loads(res["content"]["result"][0])
            if result["success"] == "ok":
                return True
            else:
                return False
        else:
            return False

    def _send_push_request(self, desp, key, server, text, type):
        return requests.get(server + self.endpoint, params={
            "pushkey": key,
            "text": text,
            "type": type,
            "desp": desp,
        }).json()

    def send_text(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                  pushkey: Union[str, list, None] = None):
        """
        Any text are accepted when type is text.
        @param text: message : text
        @param desp: the second part of the message (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(text=text, desp=desp, server=server, pushkey=pushkey, text_type='text')

    def send_markdown(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                      pushkey: Union[str, list, None] = None):
        """
        Text in Markdown format are accepted when type is markdown.
        @param text: message : text in markdown
        @param desp: the second part of the message in markdown (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(text=text, desp=desp, server=server, pushkey=pushkey, text_type='markdown')

    def send_image(self, image_src: str, desp: Optional[str] = None, server: Optional[str] = None,
                   pushkey: Union[str, list, None] = None):
        """
        Only image src are accepted by API now, when type is image.
        @param image_src: message : image URL
        @param desp: the second part of the message (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(text=image_src, desp=desp, server=server, pushkey=pushkey, text_type='image')
