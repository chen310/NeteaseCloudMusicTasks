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
            exec('{}.push(data["title"], data["mdmsg"], data["mdmsg_compat"], data["textmsg"], config)'.format(
                config['module']))
            return

        # 配置相同才会合并推送
        key = eval('{}.getKey(data)'.format(config['module']))
        if key is not None:
            if key in self.datas:
                for syntax in ['mdmsg', 'mdmsg_compat', 'textmsg']:
                    self.datas[key][syntax] += self.separator
                    self.datas[key][syntax] += data[syntax]
            else:
                self.datas[key] = data

    def push(self):
        for data in self.datas.values():
            exec('{}.push(data["title"], data["mdmsg"], data["mdmsg_compat"], data["textmsg"], data["config"])'.format(
                data['config']['module']))
