#!/bin/bash
set -u
#set -eu
#set -o pipefail

trap 'echo "error:$0($LINENO) \"$BASH_COMMAND\" \"$@\""' ERR

TAG="アズールレーン"
DATE=$(date +'%Y%m%d%H%M%S')

echo "start: $(date +'%Y-%m-%d %H:%M:%S')" >> download_latest.log 2>&1

python3 pixiv_tag_download.py "${TAG}" "${HOME}/pixiv_data/image_" >> download_latest.log 2>&1
RES=$?

echo "end: ${RES} $(date +'%Y-%m-%d %H:%M:%S')" >> download_latest.log 2>&1

cp download_latest.log "download_${TAG}_${DATE}.log"

