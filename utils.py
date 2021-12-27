import copy
import json


def updateConfig(src, dst):
    target = copy.deepcopy(dst)
    if isinstance(src, dict):
        for key in src:
            if key in target:
                target[key] = updateConfig(src[key], target[key])
            else:
                target[key] = src[key]
    elif isinstance(src, list):
        if len(src) == 0:
            target = src
        else:
            if len(target) == 0:
                target = copy.deepcopy(src)
            else:
                if isinstance(src[0], dict):
                    t = target[0]
                    target = []
                    for item in src:
                        target.append(updateConfig(item, t))
                else:
                    target = copy.deepcopy(src)
    else:
        target = copy.deepcopy(src)
    return target


def jsonDumps(data):
    return json.dumps(data, indent=4, ensure_ascii=False)
