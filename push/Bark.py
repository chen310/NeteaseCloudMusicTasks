import requests
from urllib import parse


def getKey(data):
    config = data['config']
    if len(config['Bark_key']) == 0:
        return None
    return (config['module'], config['Bark_key'])


def push(title, mdmsg, mdmsg_compat, textmsg, config):
    msg = mdmsg
    Bark_key = config['Bark_key']
    Bark_url = config['Bark_url']
    if len(Bark_key) == 0 and len(Bark_url) == 0:
        return
    url = parse.urljoin(Bark_url, Bark_key)

    requests.post(url, data={"title": title, "body": msg})
