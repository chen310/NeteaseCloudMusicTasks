import os

if __name__ == "__main__":
    github_url = 'https://github.com/chen310/NeteaseCloudMusicTasks.git'
    scripts_config = '/ql/scripts/chen310_NeteaseCloudMusicTasks/config.json'
    old_config = '/ql/scripts/chen310_NeteaseCloudMusicTasks/config.old.json'
    example_config = '/ql/scripts/chen310_NeteaseCloudMusicTasks/config.example.json'
    repo_config = '/ql/repo/chen310_NeteaseCloudMusicTasks/config.json'
    dependencies = '/ql/repo/chen310_NeteaseCloudMusicTasks/requirements.txt'
    if os.path.exists(scripts_config):
        print('备份配置文件...')
        os.system('cp -f {} {}'.format(scripts_config, old_config))
        print('复制配置示例文件...')
        os.system('cp -f {} {}'.format(repo_config, example_config))
        print('更新配置文件...')
        os.system('python3 /ql/scripts/chen310_NeteaseCloudMusicTasks/serverless/loadconfig.py {} {} {}'.format(
            repo_config, scripts_config, scripts_config))
        print('更新完成')
    else:
        print('复制配置文件')
        os.system('cp {} {}'.format(repo_config, scripts_config))
        print('复制配置示例文件...')
        os.system('cp -f {} {}'.format(repo_config, example_config))

    try:
        import requests
        import json5
        from Cryptodome.Cipher import AES
    except:
        print('安装依赖...')
        os.system('apk update')
        os.system('apk upgrade')
        os.system('apk add gcc libc-dev')
        os.system('pip3 install -r {}'.format(dependencies))
