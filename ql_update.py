import os
import json5

if __name__ == "__main__":
    os.system(
        'ql repo https://github.com/chen310/NeteaseCloudMusicTasks "index.py" "" "py"')
    os.system('python3 ./serverless/loadconfig.py /ql/repo/chen310_NeteaseCloudMusicTasks/config.json ./config.json ./config.json')
    print("配置文件更新成功")
