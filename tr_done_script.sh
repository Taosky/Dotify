#!/bin/sh

PARAM=$(echo $TR_TORRENT_DIR | tr -d '\n' | xxd -plain | sed 's/\(..\)/%\1/g' | tr -d "\n")

curl "http://127.0.0.1:4023/downloaded?dir=$PARAM" -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3' --compressed -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0'
