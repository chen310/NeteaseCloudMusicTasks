import json
import json5
import re
import copy
import sys

key_list = ['version', 'desp']

def copy_config(src, dst):
    target = copy.deepcopy(dst)
    if isinstance(src, dict):
        for key in src:
            if key in target:
                if key not in key_list:
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


config = json5.load(open(sys.argv[1], 'r', encoding='utf-8'))
oldconfig = json5.load(open(sys.argv[2], 'r', encoding='utf-8'))

data = copy_config(oldconfig, config)
with open(sys.argv[1], 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
