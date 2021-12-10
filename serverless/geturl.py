import json
import sys
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client, models
try:
    cred = credential.Credential(sys.argv[1], sys.argv[2])
    httpProfile = HttpProfile()
    httpProfile.endpoint = "scf.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = scf_client.ScfClient(cred, sys.argv[4], clientProfile)

    req = models.GetFunctionAddressRequest()
    params = {
        "FunctionName": sys.argv[3]
    }
    req.from_json_string(json.dumps(params))

    resp = client.GetFunctionAddress(req)
    print(resp.Url)

except TencentCloudSDKException as err:
    print("ERROR:" + str(err))
