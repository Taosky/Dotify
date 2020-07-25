# TransmissionNotify
用于Transmission 下载完成后推送电影信息，包括Bark、Telegram...


## Features
- Transmission路径API
- 豆瓣登录获取信息
- Telegram推送
- Bark推送
- Telegram代理


## 使用说明
1. 配置运行本程序
2. 修改Transmission配置参数`script-torrent-done-filename`
3. 新建Transmission脚本
```bash
#!/bin/sh
PARAM=$(echo $TR_TORRENT_DIR | tr -d '\n' | xxd -plain | sed 's/\(..\)/%\1/g' | tr -d "\n")

curl "http://<IP或域名>/downloaded?token=<配置文件设置的token>&dir=$PARAM" -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3' --compressed -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0'

```
