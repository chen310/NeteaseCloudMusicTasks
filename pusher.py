import os

for file in os.listdir(os.path.join(os.path.dirname(__file__), 'push')):
    if not file.startswith('_') and file.endswith('py'):
        exec('from push import {}'.format(file.replace('.py', '')))


class Pusher():
    def __init__(self):
        self.datas = {}
        self.separator = '-------------------------\n'

    def append(self, data):
        config = data['config']
        # 是否开启推送
        if not config['enable']:
            return
        # 是否合并推送
        if not config['merge']:
            exec('{}.push(data["title"], data["mdmsg"], data["textmsg"], config)'.format(
                config['module']))
            return

        # 配置相同才会合并推送
        key = eval('{}.getKey(data)'.format(config['module']))
        if key is not None:
            if key in self.datas:
                self.datas[key]['mdmsg'] += self.separator
                self.datas[key]['mdmsg'] += data['mdmsg']
                self.datas[key]['textmsg'] += self.separator
                self.datas[key]['textmsg'] += data['textmsg']
            else:
                self.datas[key] = data

    def push(self):
        for data in self.datas.values():
            exec('{}.push(data["title"], data["mdmsg"], data["textmsg"], data["config"])'.format(
                data['config']['module']))
