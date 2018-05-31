#!/bin/bash
set -u
#set -eu
#set -o pipefail

trap 'echo "error:$0($LINENO) \"$BASH_COMMAND\" \"$@\""' ERR

TAG="鳩羽つぐ"
DATE=$(date +'%Y%m%d_%H%M%S')

echo "start: $(date +'%Y-%m-%d %H:%M:%S')" 2>&1 | tee download_latest.log

python3 pixiv_tag_download.py "${TAG}" "${HOME}/pixiv_data/image_" 2>&1 | tee -a download_latest.log
RES=$?

echo "end: ${RES} $(date +'%Y-%m-%d %H:%M:%S')" 2>&1 | tee -a download_latest.log

cp download_latest.log "download_${TAG}_${DATE}.log"

