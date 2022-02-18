import copy
import json
import os


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


def append_environ(vars):
    if 'TENCENT_SECRET_ID' not in os.environ or 'TENCENT_SECRET_KEY' not in os.environ:
        print('环境变量 TENCENT_SECRET_ID 或 TENCENT_SECRET_KEY 不存在。项目地址: https://github.com/chen310/NeteaseCloudMusicTasks')
        return False
    kv = {}
    keylist = ["TENCENT_SECRET_ID", "TENCENT_SECRET_KEY", "SONG_NUMBER"]
    for key in os.environ:
        if key in keylist:
            kv[key] = os.environ.get(key)
        elif 'COOKIE' in key:
            kv[key] = os.environ.get(key)

    kv.update(vars)
    Variables = []
    for key in kv:
        Variables.append({"Key": key, "Value": kv[key]})

    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.scf.v20180416 import scf_client, models

    try:
        cred = credential.Credential(os.environ.get(
            "TENCENT_SECRET_ID"), os.environ.get("TENCENT_SECRET_KEY"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "scf.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, os.environ.get(
            "TENCENTCLOUD_REGION"), clientProfile)

        req = models.UpdateFunctionConfigurationRequest()
        params = {
            "FunctionName": os.environ.get("SCF_FUNCTIONNAME"),
            "Environment": {
                "Variables": Variables
            }
        }
        req.from_json_string(json.dumps(params))

        resp = client.UpdateFunctionConfiguration(req)
        print(resp.to_json_string())
        return True

    except TencentCloudSDKException as err:
        print(err)
        return False
