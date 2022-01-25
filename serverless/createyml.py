import json
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client, models


def getEnv(name, default=""):
    if name in os.environ and len(os.environ.get(name)) > 0:
        return os.environ.get(name)
    else:
        return default


def makeTimer(name, cron, enable=True, arg=""):
    timer = "    - timer:\n"
    timer += "        name: " + name + "\n"
    timer += "        parameters:\n"
    timer += "          cronExpression: \"" + cron + "\"\n"
    if enable:
        timer += "          enable: true\n"
    else:
        timer += "          enable: false\n"
    if len(arg) > 0:
        timer += "          argument: \"" + arg + "\"\n"
    return timer


try:
    envs = []
    triggers = []
    if os.environ.get("DEPLOY_TYPE") == "update":
        cred = credential.Credential(
            getEnv("TENCENT_SECRET_ID"), getEnv("TENCENT_SECRET_KEY"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "scf.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = scf_client.ScfClient(cred, getEnv(
            "REGION", getEnv("DEFAULT_REGION")), clientProfile)

        # 函数信息
        req = models.GetFunctionRequest()
        params = {
            "FunctionName": getEnv("FUNCTION_NAME", getEnv("DEFAULT_FUNCTION_NAME"))
        }
        req.from_json_string(json.dumps(params))

        resp = client.GetFunction(req)
        data = json.loads(resp.to_json_string())
        envs = data["Environment"]["Variables"]

        # 触发器
        req = models.ListTriggersRequest()
        params = {
            "FunctionName": getEnv("FUNCTION_NAME", getEnv("DEFAULT_FUNCTION_NAME"))
        }
        req.from_json_string(json.dumps(params))

        resp = client.ListTriggers(req)
        triggers = json.loads(resp.to_json_string()).get("Triggers", [])

    with open("serverless.yml", "w") as f:
        f.write("app: " + getEnv("FUNCTION_NAME",
                getEnv("DEFAULT_FUNCTION_NAME")) + "\n")
        f.write("component: scf\n")
        f.write("name: " + getEnv("FUNCTION_NAME",
                getEnv("DEFAULT_FUNCTION_NAME")) + "\n")
        f.write("inputs:\n")
        f.write("  name: " + getEnv("FUNCTION_NAME",
                getEnv("DEFAULT_FUNCTION_NAME")) + "\n")
        f.write("  description: 网易云音乐自动任务\n")
        f.write("  src: ./\n")
        f.write("  handler: index.main_handler\n")
        f.write("  runtime: Python3.6\n")
        f.write("  region: " + getEnv("REGION", getEnv("DEFAULT_REGION")) + "\n")
        f.write("  memorySize: 128\n")
        f.write("  timeout: 900\n")

        f.write("  events:\n")

        mytriggers = {
            "timer-default": {
                "cron": getEnv("CRON", getEnv("DEFAULT_CRON")),
                "enable": True,
                "arg": ""
            },
            "timer-songnumber": {
                "cron": getEnv("DEFAULT_SONG_NUMER_CRON"),
                "enable": True,
                "arg": "用于每天0点获取刷歌数"
            }
        }
        for trigger in triggers:
            if trigger.get("Type", "") == "timer":
                TriggerName = trigger.get("TriggerName")
                if TriggerName in mytriggers:
                    if trigger.get("Enable") == 1:
                        mytriggers[TriggerName]['enable'] = True
                    else:
                        mytriggers[TriggerName]['enable'] = False
        for key in mytriggers:
            f.write(makeTimer(
                key, mytriggers[key]["cron"], mytriggers[key]["enable"], mytriggers[key]["arg"]))

        f.write("  environment:\n")
        f.write("    variables:\n")

        vars = {}
        for env in envs:
            vars[env['Key']] = env['Value']
        vars['TENCENT_SECRET_ID'] = getEnv("TENCENT_SECRET_ID")
        vars['TENCENT_SECRET_KEY'] = getEnv("TENCENT_SECRET_KEY")
        if 'SONG_NUMBER' not in vars:
            vars['SONG_NUMBER'] = '-1'

        for key in vars:
            f.write("      " + key + ': ' + vars[key] + "\n")


except TencentCloudSDKException as err:
    print(err)
