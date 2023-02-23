#!/bin/sh

function urlencode() {
  which "curl" >/dev/null 2>&1; if [ ! $? -eq 0 ]; then echo -E "$1";return; fi
  encode_str=$(echo -E "$1" |sed "s/%/%%/g")
  printf -- "$encode_str" | curl -Gso /dev/null -w %{url_effective} --data-urlencode @- "" |cut -c 3-
}
PARAM=$(urlencode "$TR_TORRENT_DIR")

curl "http://127.0.0.1:4023/downloaded?dir=$PARAM"
