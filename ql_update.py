import os


def writeSha(path, file):
    cur = os.getcwd()
    os.chdir(path)
    result = os.popen('git rev-parse HEAD').read().strip()
    os.chdir(cur)

    if len(result) == 40 and ' ' not in result:
        os.system('sed -i "s/commitId/{}/g" {}'.format(result, file))
        print('已写入 commit id')
    else:
        print('commit id 获取失败')


if __name__ == "__main__":
    github_url = 'https://github.com/chen310/NeteaseCloudMusicTasks.git'

    if os.path.exists('/ql/data/scripts/chen310_NeteaseCloudMusicTasks'):
        data_path = '/ql/data/'
    elif os.path.exists('/ql/scripts/chen310_NeteaseCloudMusicTasks'):
        data_path = '/ql/'
    else:
        print('未找到路径，请尝试升级青龙')
        exit(1)
    
    scripts_config =  data_path + 'scripts/chen310_NeteaseCloudMusicTasks/config.json'
    old_config = data_path + 'scripts/chen310_NeteaseCloudMusicTasks/config.old.json'
    example_config = data_path + 'scripts/chen310_NeteaseCloudMusicTasks/config.example.json'
    repo_config = data_path + 'repo/chen310_NeteaseCloudMusicTasks/config.example.json'
    dependencies = data_path + 'repo/chen310_NeteaseCloudMusicTasks/requirements.txt'
    if os.path.exists(scripts_config):
        print('备份配置文件...')
        os.system('cp -f {} {}'.format(scripts_config, old_config))
        print('复制配置示例文件...')
        os.system('cp -f {} {}'.format(repo_config, example_config))
        writeSha(os.path.dirname(repo_config), example_config)
        print('更新配置文件...')
        os.system('python3 {}scripts/chen310_NeteaseCloudMusicTasks/updateconfig.py {} {} {}'.format(
            data_path, example_config, scripts_config, scripts_config))
        print('更新完成')
    else:
        print('复制配置示例文件...')
        os.system('cp -f {} {}'.format(repo_config, example_config))
        writeSha(os.path.dirname(repo_config), example_config)
        print('复制配置文件...')
        os.system('cp {} {}'.format(example_config, scripts_config))

