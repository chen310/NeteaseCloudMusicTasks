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


try:
    cred = credential.Credential(
        getEnv("TENCENT_SECRET_ID"), getEnv("TENCENT_SECRET_KEY"))
    httpProfile = HttpProfile()
    httpProfile.endpoint = "scf.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = scf_client.ScfClient(cred, getEnv(
        "REGION", getEnv("DEFAULT_REGION")), clientProfile)

    req = models.GetFunctionAddressRequest()
    params = {
        "FunctionName": getEnv("FUNCTION_NAME", getEnv("DEFAULT_FUNCTION_NAME"))
    }
    req.from_json_string(json.dumps(params))

    resp = client.GetFunctionAddress(req)
    print(resp.Url)

except TencentCloudSDKException as err:
    print("ERROR:" + str(err))
