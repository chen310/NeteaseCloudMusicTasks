import os

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
        print('更新配置文件...')
        os.system('python3 {}scripts/chen310_NeteaseCloudMusicTasks/updateconfig.py {} {} {}'.format(
            data_path, repo_config, scripts_config, scripts_config))
        print('更新完成')
    else:
        print('复制配置文件')
        os.system('cp {} {}'.format(repo_config, scripts_config))
        print('复制配置示例文件...')
        os.system('cp -f {} {}'.format(repo_config, example_config))
