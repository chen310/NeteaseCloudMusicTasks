import json
import json5
import re
import copy


def copy_config(src, dst):
    target = copy.deepcopy(dst)
    if isinstance(src, dict):
        for key in src:
            if key in target:
                if key != 'version':
                    target[key] = copy_config(src[key], target[key])
            else:
                target[key] = src[key]
    elif isinstance(src, list):
        if len(src) == 0:
            target = src
        if len(src) > 0:
            if len(target) == 0:
                target = copy.deepcopy(src)
            else:
                if isinstance(src[0], dict):
                    t = target[0]
                    target = []
                    for item in src:
                        target.append(copy_config(item, t))
                else:
                    target = copy.deepcopy(src)
    else:
        target = copy.deepcopy(src)
    return target


config = json5.load(open('./config.json', 'r', encoding='utf-8'))
oldconfig = json5.load(open('./oldconfig.json', 'r', encoding='utf-8'))

data = copy_config(oldconfig, config)
with open('./config.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
