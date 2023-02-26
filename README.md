# Dotify
Download Notify 用于影视下载完成后（qBittorrent / Tranmission）推送信息（Bark / Telegram）

## 使用说明
1. Docker运行
```bash
docker run -d -p 4023:4023 -v /<自定义路径>/dotify:/app/data --name dotify \
--env TG_BOT_TOKEN=12345:xxxxx-xxxxx \
--env TG_CHAT_ID=123456 \
--env BARK_TOKENS=xxxxxxx_xxxxxxx_xxxxxxx \
--env PATH_REPLACE=/volume\d/Download/_http://alist.xxx.com/share/ \
--restart=always ghcr.io/taosky/dotify:latest
```
    TG_BOT_TOKEN: Telegram Bot Token
    TG_CHAT_ID: 需要发送的Chat ID
    BARK_TOKENS: Bark(IOS) Token, 以`_`分隔(单个也需要最后加上`_`)
    PATH_REPLACE: 正则替换一段路径, 以`_`分割正则和替换文本 (如替换本地下载路径为alist页面的路径)

    MOVIE_DIR_RE: 影视文件夹的正则匹配, 默认为`(.*?)（(\d{4})）`, 即下载路径的文件夹须类似`狂飙（2023）`

2. 下载脚本[tr_done.sh](https://raw.githubusercontent.com/Taosky/Dotify/master/tr_done.sh) / [qb_done.sh](https://raw.githubusercontent.com/Taosky/Dotify/master/qb_done.sh), 修改权限以便执行
3. 在webui进行设置, Transmission在`下载完成后执行脚本`输入路径`/your path/tr_done.sh`, qBittorrent在`torrent 完成时运行外部程序`输入路径加参数`/your path/qbit_done.sh "%D"`
