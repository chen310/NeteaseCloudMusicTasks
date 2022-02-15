# 网易云打卡升级

<p>
  <a href="https://music.163.com/#/user/home?id=347837981"><img alt="网易云音乐关注数" src="https://img.shields.io/badge/dynamic/json?color=e60026&label=%E7%BD%91%E6%98%93%E4%BA%91%E9%9F%B3%E4%B9%90&query=%24.profile.followeds&url=http%3A%2F%2Fmusic.163.com%2Fapi%2Fv1%2Fuser%2Fdetail%2F347837981"></a>
  <a href="http://www.coolapk.com/u/3189084"><img alt="酷安关注数" src="https://img.shields.io/badge/dynamic/json?color=0eb066&label=%E9%85%B7%E5%AE%89&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dcoolapk%26queryKey%3D3189084"></a>
</p>

## 功能

1. 签到领云贝
2. 自动完成云贝任务，并领取云贝
3. 打卡升级
4. 刷指定歌曲的播放量
5. 音乐人自动签到领取云豆
6. 音乐人自动完成任务，并领取云豆
7. 自动领取 vip 成长值（任务需自己完成）
8. 多种推送方式
9. 支持多账号
10. 支持[腾讯云函数](#一部署到腾讯云函数) & [青龙面板](#二部署到青龙面板) & [本地运行](#三本地运行) & [docker 部署](#四使用docker部署)

> 开发不易，如果你觉得本项目对你有用，可以点个 star，也可以到底部给个[赞赏](#赞赏)

## 一、部署到腾讯云函数

### 开通服务

首次使用云函数，依次登录 [SCF 云函数控制台](https://console.cloud.tencent.com/scf) 和 [SLS 控制台](https://console.cloud.tencent.com/sls) 开通相关服务，确保账户下已开通服务并创建相应[服务角色](https://console.cloud.tencent.com/cam/role) **SCF_QcsRole、SLS_QcsRole**

> 注意！为了确保权限足够，获取这两个参数时不要使用子账户！此外，腾讯云账户需要[实名认证](https://console.cloud.tencent.com/developer/auth)。

### 获取密钥

在腾讯云[API 密钥管理](https://console.cloud.tencent.com/cam/capi)新建密钥，获取 SecretId 和 SecretKey

### fork 本项目

在 GitHub 上 fork [本项目](https://github.com/chen310/NeteaseCloudMusicTasks)

### 创建 Secrets

fork 之后，点击右上方 `settings`，在页面点击 `Secrets`，点击 `Actions`，然后点击 `New repository secret` 创建新的 secret。一共有 5 个 secret，前 2 个是必须要创建的，后 3 个可不创建

| Name          | Value                     | 是否必填 |
| :------------ | :------------------------ | :------- |
| SECRET_ID     | 填写之前获取的 SecretId   | 必填     |
| SECRET_KEY    | 填写之前获取的 SecretKey  | 必填     |
| FUNCTION_NAME | 自定义函数名              | 选填     |
| CRON          | 定时触发器的时间          | 选填     |
| REGION        | 地域，默认为 ap-guangzhou | 选填     |

FUNCTION_NAME 为函数名，不填写默认为 `NeteaseCloudMusicTasks`。如需更改，则创建此 secret，并填写自定义的函数名，命名规则：只能包含字母、数字、下划线、连字符，以字母开头，以数字或字母结尾，2~60 个字符。

如果之前在腾讯云函数里用上传压缩包的方式创建过该项目对应的函数，那么可以在 FUNCTION_NAME 里填写先前创建的函数名，更新会提交到先前的函数中，并自动同步配置文件。

CRON 默认为 `0 30 0 * * * *` 表示每天 0 点 30 分触发，可自行更改。比如：`0 20 12 * * * *` 表示每天 12 点 20 分触发，`0 0 12,16 * * * *` 表示每天 12 点和 16 点各触发一次。

REGION 默认为 `ap-guangzhou` ，可选的地域详见[地域列表](https://cloud.tencent.com/document/product/583/17238#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)。

### 部署

#### 自动部署

更新代码后将会自动触发 workflow，部署到腾讯云函数。到 `Actions` 中可以查看部署进度。

#### 手动部署

更新了 `Secrets` 之后不会自动部署，此时需要手动部署。击项目上方的 `Actions`，点击 `All workflows` 下方的 `deploy`（移动端要先点击 `Select workflow`），再点击右侧 `Run workflow`，在弹出的页面再次点击 `Run workflow`，将会运行新的 workflow，点进这个 workflow，可以查看部署进度。

### 添加依赖

下载[依赖文件](https://chen10.lanzouo.com/igHXzxf8wjc) ，也可以自己用 pip 下载依赖，然后打包。然后在[高级能力](https://console.cloud.tencent.com/scf/layer)新建`层`，`层名称`可以自己任意填写，然后上传刚刚下载的压缩包，点击`添加运行环境`，选择 `Python3.6`。在[函数服务](https://console.cloud.tencent.com/scf/list)点进刚刚创建的函数，点击上方的`层管理`，点击`绑定`，选择刚刚创建的层。

### 修改配置

在[函数服务](https://console.cloud.tencent.com/scf/list)点进刚刚创建的函数，在编辑器里点击 `config.json` 这个文件进行配置，可以看到文件中有红色波浪线的错误提示，可以忽略不管，也可以下拉到编辑器的右下角，点击 `JSON` 来更改语言模式，选择 `JSON with Comments`，这样就可以消除错误提示。在 `config.json` 里进行如下的账号配置。运行之后如果发现有些任务没有完成，可能是因为没有开启，将任务对应的 `enable` 字段设置为 `true` 即可开启。

#### 账号密码

```json5
"users": [
    {
        "username": "188xxxx8888",
        "countrycode": "",
        "password": "mypassword",
        "X-Real-IP": "",
        "enable": true
    }
],
// ...
```

`username` 里填写手机号或邮箱，`password` 里填写账号密码或 32 位 md5 加密后的密码，`countrycode` 为手机号前缀，使用非中国大陆的手机号登录需填写。`X-Real-IP` 里填写国内任意 IP，否则可能会有无法登录等情况出现，可填写本机 IP，查看方法为：百度搜索 ip，填写显示的 ip 即可。如果是在本地环境运行，则不需要填写 IP。`enable` 为该账号的开关，设置为 `false` 表示不运行该账号的任务。

#### 签到

```json5
"setting": {
    // ...
    "sign": true,
    // ...
}
```

签到默认开启，连续签到可以获得更多云贝。

#### 刷听歌量

```json5
"setting": {
    // ...
    "daka": {
        "enable": true,
        "full_stop": true,
        "auto": true,
        "tolerance": 10,
        "song_number": 300,
        // ...
    },
    // ...
}
```

每个账号每天最多只计算 300 首的听歌量，而且必须是没有听过的歌曲。`enable` 表示开启刷听歌量的任务，`full_stop` 表示满级后自动停止任务，无需手动将 `enable` 设为 `false`。`song_number` 表示每次要刷的歌曲数量，账号等级较低的时候可以设置得小一点，不然等级高的时候就难刷了，可能较难刷满 300 首。

`auto` 设置为 `true` 的话表示开启自动模式，程序将自动调整每次打卡的歌曲数，`song_number` 参数将失效。此时，每天 0 点时定时触发器会自动运行代码，获取当前的听歌数，并写入环境变量中，这样的话就可以比较精确地计算每次打卡的歌曲数。`tolerance` 表示对打卡误差的容忍度，在自动打卡模式下有效，如果设置为 0 表示必须要达到 300 首才停止打卡，10 表示达到 290 首就可以停止打卡。

#### 云贝任务

```json5
"setting": {
    // ...
    "yunbei_task": {
        "162005": {
            "taskName": "发布动态",
            "module": "publishEvent",
            "enable": false,
            // 需要分享的歌单id
            "id": [],
            "msg": ["每日分享","今日分享","分享歌单"],
            "delete": true
        },
        "216002": {
            "taskName": "访问云音乐商城",
            "module": "visitMall",
            "enable": true
        },
        "200002": {
            "taskName": "云贝推歌",
            "module": "rcmdSong",
            "enable": false,
            // 填写歌曲ID
            "songId": [],
            "yunbeiNum": 10,
            "reason": []
        },
        "162006": {
            "taskName": "发布Mlog",
            "module": "publishMlog",
            "enable": false,
            // 填写歌曲ID
            "songId": [],
            /* 动态内容，随机选取一个，其中$artist会被替换为歌手名，$song会被替换为歌曲名 */
            "text": [
                "分享$artist的歌曲: $song",
                "分享歌曲: $song"
            ],
            /* 图片大小，越大则消耗的外网出流量越多 */
            "size": 500,
            /* 发布成功后是否自动删除该动态 */
            "delete": true
        },
        "166000": {
            "taskName": "分享歌曲/歌单",
            "module": "share",
            "enable": false
        }
    },
    // ...
}
```

`发布动态`任务要分享歌单，可获得 5 云贝，可通过将 `enable` 设为 `true` 开启，`id` 要填写需要分享的歌单 id，可不填写，随机送推荐歌单中选取。`delete` 表示动态发布之后自动删除。

`访问云音乐商城`任务可获得 2 云贝。

`云贝推歌`任务使用云贝对喜欢的歌曲进行推荐，可获得 10 云贝。`songId` 填写喜欢的歌曲 id，如`[65528, 64634]`，程序将会随机挑选一首歌，`yunbeiNum` 是要使用的云贝数量，一般为 `10`，`reason` 填写推歌理由。

`发布Mlog` 根据填写的歌曲 ID，自动下载歌曲对应的专辑图片，并上传。`songId` 填写歌曲 id，如`[65528, 64634]`，`text` 填写动态内容

`分享歌曲/歌单`任务并不会真的分享，将 `enable` 设为 `true` 即可开启任务

#### 音乐人任务

```json5
"setting": {
    // ...
    "musician_task": {
        "399000": {
            "taskName": "登录音乐人中心",
            "module": "musicianSignin",
            "enable": true
        },
        "398000": {
            "taskName": "发布动态",
            "module": "publishEvent",
            "enable": false,
            // 自定义要分享的歌单id，用逗号隔开，分享时随机选取一个，若为空，则从每日推荐歌单中随机选取
            "id": [],
            "msg": ["每日分享","今日分享","分享歌单"],
            "delete": true
        },
        "396002": {
            "taskName": "发布主创说",
            "module": "publishComment",
            "enable": false,
            // 填写你自己歌曲的id，如有多首用,隔开，随机挑选一首
            "id": [],
            "msg": ["感谢大家收听"],
            "delete": true
        },
        "393001": {
            "taskName": "回复粉丝评论",
            "module": "replyComment",
            "enable": false,
            // 填写你自己歌曲的id，如有多首用,隔开，随机挑选一首
            "id": [],
            "msg": ["感谢收听"],
            "delete": true
        },
        "395002": {
            "taskName": "回复粉丝私信",
            "module": "sendPrivateMsg",
            "enable": false,
            // 填写粉丝的用户id，如有多个用,隔开，随机挑选一个进行回复,可以用自己的小号
            "id": [],
            "msg": ["你好"]
        }
    },
    // ...
}
```

需要是音乐人才能执行，想要开启相应的任务，需要将 `enable` 由 `false` 改为 `true`，`登录音乐人中心`自动开启，其他任务根据实际情况开启。`登录音乐人中心`即签到获取云豆；`发布动态`即转发歌单；`发布主创说`即在自己的歌曲评论区留言；`回复粉丝评论`即在自己歌曲的评论区回复粉丝留言，该任务是通过回复自己的留言实现的；`回复粉丝私信`需要填写粉丝 id，可用小号。

#### VIP 成长值任务

```json5
"setting": {
    // ...
    "709004": {
        "创建共享歌单": {
            "taskName": "创建共享歌单",
            "module": "createSharedPlaylist",
            "enable": false,
            /* 自定义歌单名，用逗号隔开，随机选取一个 */
            "name": [
                "歌单",
                "我的歌单"
            ],
            /* 创建成功后是否自动删除该动态 */
            "delete": true
        }
    },
    // ...
}
```

`创建共享歌单` 任务默认关闭，需要开启的话将 `enable` 设为 `true`，`name` 里填写自定义的歌单名，创建时随机选取一个，`delete`表示歌单创建成功后时候自动删除。

#### 推送

支持多种推送方式，建议使用企业微信进行推送

1. 企业微信
2. server 酱
3. 酷推
4. pushPlus
5. Telegram
6. [Bark](https://github.com/Finb/Bark)

要使用推送的话将相应的 `enable` 设为 `true`，并填写配置

##### 企业微信

```json5
"WeCom": {
    "module": "WeCom",
    "enable": false,
    "corpid": "",
    "agentid": "",
    "secret": "",
    "userid": "@all",
    "msgtype": "text",
    /* 是否将多个账号的信息合并推送 */
    "merge": false
}
```

注册企业微信账号可参考[这里](https://sct.ftqq.com/forward)

`corpid` 为企业 ID，登录企业微信后在管理后台`我的企业`－`企业信息`下查看；`agentid` 为应用 ID，在`应用管理`里，点进相应的应用可查看；`secret` 为应用密钥，在`应用管理`里，点进相应的应用可查看；`userid` 默认为`@all`，会向该企业应用的全部成员发送；`msgtype` 为消息类型，可填写文本消息 `text`、文本卡片消息 `textcard` 或 markdown 消息 `markdown`，markdown 消息不能在微信里查看，只能在企业微信里查看。

##### server 酱

```json5
"serverChan": {
    "module": "serverChan",
    "enable": false,
    "KEY": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用 server 酱的话需要在 `KEY` 里填写旧版的 SCKEY 或新版的 SendKey。

##### 酷推

```json5
"CoolPush": {
    "module": "CoolPush",
    "enable": false,
    /* 推送方式: send QQ号私人推送 | group QQ群推送 | wx 微信推送 | email 邮件推送 */
    "method": "send",
    "Skey": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用酷推的话需要填写 `Skey`。

##### pushPlus 微信推送

```json5
"pushPlus": {
    "module": "pushPlus",
    "enable": false,
    "pushToken": "",
    /* 消息模板:  markdown | html | txt | json */
    "template": "markdown",
    /* 群组编码，为空时发给自己 */
    "topic": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用酷推的话需要填写 `pushToken`。

##### Telegram 推送

```json5
"Telegram": {
    "module": "Telegram",
    "enable": false,
    /* Telegram账号ID */
    "userId": "",
    /* TG机器人token */
    "botToken": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用 Telegram 的话需要填写 `userId` 和 `botToken`。

##### Bark 推送

```json5
"Bark": {
    "module": "Bark",
    /* 是否启用Bark推送 */
    "enable": false,
    /* Bark的地址 */
    "Bark_url": "",
    /* Bark的API key */
    "Bark_key": "",
    /* 是否将多个账号的信息合并推送, 建议为false，iOS推送消息过长可能会失败 */
    "merge": false
}
```

要使用 Bark 的话需要填写 `Bark_url` 和 `Bark_key`。可以使用 Bark 官方 API 或者自行搭建。

#### 刷单曲播放量

```json5
"setting": {
    // ...
    "other": {
        /* 刷歌单中歌曲的播放次数，用来改变听歌风格，仅在需要时使用 */
        "play_playlists": {
            "enable": false,
            /* 歌单id,用逗号隔开,如 [5279371062,5279377564] */
            "playlist_ids": [],
            /* 播放次数 */
            "times": 1
        }
    },
    // ...
}
```

将要刷的歌曲加到歌单中，把歌单 id 填写到 `playlist_ids` 中，可以添加多个歌单 id，用英文逗号隔开，如 `"playlist_ids":[5279371062,5279377564]`。该功能可以用来改变听歌风格。

#### 多账号

```json5
"users": [
    {
        "username": "188xxxx8888",
        "md5": false,
        "password": "mypassword"
    },
    {
        "username": "166xxxx6666",
        "md5": false,
        "password": "anotherpassword"
    }
],
// ...
```

多账号需要删除第二个账号前后的`\*`和`*\`注释，如上所示。如果不会使用，可以每个账号创建一个相应的云函数。

假如多个账号配置不同可以参照下面

```json5
"users": [
    {
        "username": "188xxxx8888",
        "md5": false,
        "password": "mypassword"
    },
    {
        "username": "166xxxx6666",
        "md5": false,
        "password": "anotherpassword",
        "setting": {
            "serverChan": {
                "KEY": "xxxxxxxxxx"
            },
            "yunbei_task": {
                "云贝推歌": {
                    "songId": [25707139],
                }
            },
        }
    }
],
// ...
```

如上所示，在第二个账号中加入了 `setting` 字段，并填写与公共配置不同的地方。这样一来，两个账号就使用了不同的 server 酱推送，并使用不同的歌曲进行云贝推歌。

#### 关注作者

```json5
"setting": {
    // ...
    "follow": true
    // ...
}
```

默认会在网易云音乐中关注我，不喜欢的可自行取消。

### 测试

修改完代码后，按 ctrl+s 保存代码，然后点击编辑器右上角的`部署`（每次修改完都要重新部署），左下角的`部署`也行。部署完成后点击部署旁边的测试按钮，观察结果，如果失败则检查修改代码。

[计费方式](https://cloud.tencent.com/document/product/628/39300)

### 更新代码

在 GitHub 项目页面点击 `Fetch upstream` - `Fetch and merge`，然后再到 `Actions` 中[部署](#部署)。重新部署之后，配置文件自动同步，无需再次填写，但注释会被删除，如果需要修改配置文件，可以参考 `config.example.json` 文件中的注释。进入到云函数中时，如果提醒“检测到当前工作区函数和已部署函数不一致，重新加载已部署函数?”，点击`确认`即可。

更新代码后将会自动部署到腾讯云函数，但修改了 Secrets 之后需要手动部署，详见[部署](#部署)。

## 二、部署到青龙面板

### 拉取仓库

```shell
ql repo https://github.com/chen310/NeteaseCloudMusicTasks.git "index.py" "" "py" && task /ql/scripts/chen310_NeteaseCloudMusicTasks/ql_update.py
```

第一次使用需要安装依赖，时间可能会长一些

更新代码同样也是用上面的命令

### 修改配置文件

对配置文件 `config.json` 文件进行修改

## 三、本地运行

### 下载

```shell
git clone https://github.com/chen310/NeteaseCloudMusicTasks.git
```

### 安装依赖

```shell
pip install -r requirements.txt
```

### 运行

```shell
python index.py
```

## 四、使用`docker`部署

> 1. 支持 ARM64/AMD64 docker 镜像
> 2. 支持指定时间定时执行
> 3. 未指定定时执行时间，每次重启随机设定执行时间

### 下载并配置 `config.json`

```shell
curl -fsSL -o config.json https://raw.githubusercontent.com/chen310/NeteaseCloudMusicTasks/main/config.json
```

### 随机时间执行

```shell
docker run -itd --restart=on-failure \
    -v $(pwd)/config.json:/root/config.json \
    --name netease-cloud-music-tasks \
    enwaiax/netease-cloud-music-tasks:latest
```

### 指定时间执行

```shell
docker run -itd --restart=on-failure \
    -v $(pwd)/config.json:/root/config.json \
    -e "SCHEDULER_HOUR=8" -e "SCHEDULER_MINUTE=30" \
    --name netease-cloud-music-tasks \
    enwaiax/netease-cloud-music-tasks:latest
```

## 其他

### 对日推的影响

打卡功能可能会影响日推，介意慎用。

### 云函数免费额度及计费方式

在云函数[概览](https://console.cloud.tencent.com/scf/index)界面，可以查看本月剩余免费额度

详见[计费概述](https://cloud.tencent.com/document/product/583/17299)

### 赞赏

<p align="left">微信</p> <img width="300" height="300" src="https://cdn.jsdelivr.net/gh/chen310/NeteaseCloudMusicTasks/public/img/wechatpay.png" />

<p align="left">支付宝</p> <img width="300" height="300" src="https://cdn.jsdelivr.net/gh/chen310/NeteaseCloudMusicTasks/public/img/alipay.png" />

<p align="left">支付宝领红包</p> <img width="300" height="300" src="https://cdn.jsdelivr.net/gh/chen310/NeteaseCloudMusicTasks/public/img/alipayhb.png" />

<p align="left">饿了么领红包</p> <img width="300" height="300" src="https://cdn.jsdelivr.net/gh/chen310/NeteaseCloudMusicTasks/public/img/eleme.png" />

### star 数

[![Stargazers over time](https://starchart.cc/chen310/NeteaseCloudMusicTasks.svg)](https://starchart.cc/chen310/NeteaseCloudMusicTasks)

### 声明

- 本仓库中的脚本仅用于测试和学习目的，请勿用于商业或非法目的，否则后果自负
- 如果您认为该项目的脚本可能涉嫌侵犯您的权利，请及时通知，我们将在确认后及时删除

### 灵感来源

1. [网易云音乐 API](https://github.com/Binaryify/NeteaseCloudMusicApi)
2. [NetEase-MusicBox](https://github.com/darknessomi/musicbox)
