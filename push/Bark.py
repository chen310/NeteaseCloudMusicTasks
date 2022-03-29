import requests
from urllib import parse


def getKey(data):
    config = data['config']
    if len(config['Bark_key']) == 0 or len(config['Bark_url']) == 0:
        return None
    return (config['module'], config['Bark_key'], config['Bark_url'], config['sound'], config['group'], config['icon'])


def push(title, mdmsg, textmsg, config):
    msg = mdmsg
    Bark_key = config['Bark_key']
    Bark_url = config['Bark_url']
    if len(Bark_key) == 0 and len(Bark_url) == 0:
        return
    url = parse.urljoin(Bark_url, Bark_key)
    data = {"title": title, "body": msg}
    if config['sound']:
        data['sound'] = config['sound']
    if config['group']:
        data['group'] = config['group']
    if config['icon']:
        data['icon'] = config['icon']

    requests.post(url, data=data)
